import matplotlib.axes as axs
import matplotlib.backend_bases as bb
import matplotlib.collections as coll
import matplotlib.pyplot as plt
import matplotlib.text as txt
import numpy as np
import pandas as pd
import unittest
from unittest.mock import patch
import sys
import warnings

# make utility scripts visible
sys.path.append('scm_modules/utils/')
import DataSeriesUtility as dsu
import FileUtility as fut

sys.path.append('scm_modules/metrics/')
from main_sequence import MainSequence


def createUUT():
    '''
    Returns an initialized object to test (no directory-path required for testing)
    '''
    return MainSequence('')


class TestMainSequenceAnnotatePoint(unittest.TestCase):
    @patch('matplotlib.collections.PathCollection.contains')
    @patch('matplotlib.text.Text.set_visible')
    @patch('matplotlib.text.Text.get_visible')
    def testCorrectFunctionCallsIfSinglePointSelected(self, mocked_txt_get_vis_func, mocked_txt_set_vis_func,
                                                      mocked_coll_cont_func):
        '''
        Test correct function calls if mouse hovers over a single scattered point
        '''
        # assert mocks
        self.assertIs(txt.Text.get_visible, mocked_txt_get_vis_func)
        self.assertIs(txt.Text.set_visible, mocked_txt_set_vis_func)
        self.assertIs(coll.PathCollection.contains, mocked_coll_cont_func)

        # create mock values
        mocked_ax = plt.gca()
        mocked_ax.set_xlim((0, 1))
        mocked_ax.set_ylim((0, 1))
        mocked_scatter = mocked_ax.scatter(pd.Series([.5], dtype=float), pd.Series([.5], dtype=float))
        mocked_coll_cont_func.return_value = True, {'ind': np.array([0], dtype=int)}
        mocked_annotation_points_list = [
            txt.Annotation('dummy-annotation1', (.5, .5), visible=False),
            txt.Annotation('dummy-annotation2', (.1, .5), visible=False),
            txt.Annotation('dummy-annotation3', (.7, .2), visible=False)
        ]
        mocked_mouse_event = bb.MouseEvent('mocked-mouse-event', plt.gcf().canvas, 322, 242)  # on point (.5|.5)

        # create object
        main_sequence = createUUT()
        with patch.object(main_sequence, '_annotation_points', mocked_annotation_points_list):
            # call function to test
            main_sequence._annotate_point(mocked_mouse_event, mocked_scatter)

            # assert function calls
            mocked_coll_cont_func.assert_called_once()
            call_list = [mocked_txt_get_vis_func(), mocked_txt_get_vis_func(), mocked_txt_get_vis_func()]
            mocked_txt_get_vis_func.has_calls(call_list)  # called three times
            mocked_txt_set_vis_func.assert_called()

    @patch('matplotlib.collections.PathCollection.contains')
    @patch('matplotlib.text.Text.set_visible')
    @patch('matplotlib.text.Text.get_visible')
    def testCorrectFunctionCallsIfPointNotSelected(self, mocked_txt_get_vis_func, mocked_txt_set_vis_func,
                                                   mocked_coll_cont_func):
        '''
        Test correct function calls if point is not contained in any scattered point but in axes-view
        '''
        # assert mocks
        self.assertIs(txt.Text.get_visible, mocked_txt_get_vis_func)
        self.assertIs(txt.Text.set_visible, mocked_txt_set_vis_func)
        self.assertIs(coll.PathCollection.contains, mocked_coll_cont_func)

        # create mock values
        mocked_ax = plt.gca()
        mocked_ax.set_xlim((0, 1))
        mocked_ax.set_ylim((0, 1))
        mocked_scatter = mocked_ax.scatter(pd.Series([.5], dtype=float), pd.Series([.5], dtype=float))
        mocked_coll_cont_func.return_value = False, {'ind': np.array([])}
        mocked_annotation_points_list = [
            txt.Annotation('dummy-annotation', (.5, .5), visible=False),
            txt.Annotation('dummy-annotation2', (.1, .5), visible=False),
            txt.Annotation('dummy-annotation3', (.7, .2), visible=False)
        ]
        mocked_mouse_event = bb.MouseEvent('mocked-mouse-event', plt.gcf().canvas, 100, 200)  # not on point (.5|.5)
        mocked_txt_get_vis_func.return_value = True

        # create object
        main_sequence = createUUT()
        with patch.object(main_sequence, '_annotation_points', mocked_annotation_points_list):
            # call function to test
            main_sequence._annotate_point(mocked_mouse_event, mocked_scatter)

            # assert function calls
            mocked_coll_cont_func.assert_called_once()
            call_list = [mocked_txt_get_vis_func(), mocked_txt_get_vis_func(), mocked_txt_get_vis_func()]
            mocked_txt_get_vis_func.has_calls(call_list)  # called three times
            mocked_txt_set_vis_func.assert_called()  # called several times

    def testCorrectSettingOfMultipleAnnotationPoints(self):
        '''
        Test correct setting of annotations if mouse hovers over multiple scattered points
        '''
        # create mock values
        mocked_ax = plt.gca()
        mocked_ax.set_xlim((0, 1))
        mocked_ax.set_ylim((0, 1))
        mocked_scatter = mocked_ax.scatter(pd.Series([.5, .5, .5], dtype=float), pd.Series([.5, .5, .5], dtype=float))
        # 3 annotations on same point
        mocked_annotation_points_list = [
            txt.Annotation('dummy-annotation1', (.5, .5), visible=False),
            txt.Annotation('dummy-annotation2', (.5, .5), visible=False),
            txt.Annotation('dummy-annotation3', (.5, .5), visible=False)
        ]
        mocked_last_hov_index = -1
        mocked_mouse_event_on = bb.MouseEvent('mocked-mouse-event-on', plt.gcf().canvas, 322, 242)  # on point (.5|.5)
        mocked_mouse_event_off = bb.MouseEvent('mocked-mouse-event-off', plt.gcf().canvas, 100, 100)  # off point (.5|.5)

        # create object
        main_sequence = createUUT()
        with patch.object(main_sequence, '_annotation_points', mocked_annotation_points_list):
            with patch.object(main_sequence, '_last_hov_anno_index', mocked_last_hov_index):
                # call function on point
                main_sequence._annotate_point(mocked_mouse_event_on, mocked_scatter)

                # assert last hovered index
                self.assertEqual(0, main_sequence._last_hov_anno_index)
                self.assertTrue(main_sequence._annotation_points[0].get_visible())

                # call function off point
                main_sequence._annotate_point(mocked_mouse_event_off, mocked_scatter)

                # assert last hovered index (no change in index off point)
                self.assertEqual(0, main_sequence._last_hov_anno_index)
                self.assertFalse(main_sequence._annotation_points[0].get_visible())

                # call function on point again (annotation should change)
                main_sequence._annotate_point(mocked_mouse_event_on, mocked_scatter)

                # assert last hovered index change
                self.assertEqual(1, main_sequence._last_hov_anno_index)
                self.assertTrue(main_sequence._annotation_points[1].get_visible())

    def testCorrectSettingOfMultipleAnnotationPointsOfAnotherGroup(self):
        '''
        Test correct setting of annotations if mouse hovers from one group of annotation points to another
        '''
        # create mock values
        mocked_ax = plt.gca()
        mocked_ax.set_xlim((0, 1))
        mocked_ax.set_ylim((0, 1))
        mocked_scatter = mocked_ax.scatter(pd.Series([.5, .5, .25, .25], dtype=float),
                                           pd.Series([.5, .5, .25, .25], dtype=float))
        # 2 annotations on same point
        mocked_annotation_points_list = [
            txt.Annotation('dummy-annotation1_1', (.5, .5), visible=False),
            txt.Annotation('dummy-annotation1_2', (.5, .5), visible=False),
            txt.Annotation('dummy-annotation2_1', (.25, .25), visible=False),
            txt.Annotation('dummy-annotation2_2', (.25, .25), visible=False),
        ]
        mocked_last_hov_index = -1
        mocked_mouse_event_on_1 = bb.MouseEvent('mocked-mouse-event-on-1', plt.gcf().canvas, 322, 242)  # on point (.5|.5)
        mocked_mouse_event_on_2 = bb.MouseEvent('mocked-mouse-event-on-2', plt.gcf().canvas, 205, 146)  # on point (.25|.25)
        mocked_mouse_event_off = bb.MouseEvent('mocked-mouse-event-off', plt.gcf().canvas, 100, 100)  # off points

        # create object
        main_sequence = createUUT()
        with patch.object(main_sequence, '_annotation_points', mocked_annotation_points_list):
            with patch.object(main_sequence, '_last_hov_anno_index', mocked_last_hov_index):
                # call function on point 1
                main_sequence._annotate_point(mocked_mouse_event_on_1, mocked_scatter)

                # assert last hovered index
                self.assertEqual(0, main_sequence._last_hov_anno_index)
                self.assertTrue(main_sequence._annotation_points[0].get_visible())

                # call function off point
                main_sequence._annotate_point(mocked_mouse_event_off, mocked_scatter)

                # assert last hovered index (no change in index off point)
                self.assertEqual(0, main_sequence._last_hov_anno_index)
                self.assertFalse(main_sequence._annotation_points[0].get_visible())

                # call function on point 2
                main_sequence._annotate_point(mocked_mouse_event_on_2, mocked_scatter)

                # assert last hovered index change
                self.assertEqual(2, main_sequence._last_hov_anno_index)
                self.assertTrue(main_sequence._annotation_points[2].get_visible())


class TestMainSequenceLayoutAx(unittest.TestCase):
    @patch('matplotlib.axes.Axes.set_xlim')
    @patch('matplotlib.axes.Axes.set_ylim')
    @patch('matplotlib.axes.Axes.plot')
    @patch('matplotlib.axes.Axes.add_artist')
    @patch('matplotlib.axes.Axes.annotate')
    @patch('matplotlib.axes.Axes.set_xlabel')
    @patch('matplotlib.axes.Axes.set_ylabel')
    def testCorrectFunctionCalls(self, mocked_ax_ylabel_func, mocked_ax_xlabel_func, mocked_ax_anno_func,
                                 mocked_ax_add_art_func, mocked_ax_plot_func, mocked_ax_ylim_func, mocked_ax_xlim_func):
        '''
        Test that correct functions are invoked
        '''
        # assert mocks
        self.assertIs(axs.Axes.set_xlim, mocked_ax_xlim_func)
        self.assertIs(axs.Axes.set_ylim, mocked_ax_ylim_func)
        self.assertIs(axs.Axes.plot, mocked_ax_plot_func)
        self.assertIs(axs.Axes.add_artist, mocked_ax_add_art_func)
        self.assertIs(axs.Axes.annotate, mocked_ax_anno_func)
        self.assertIs(axs.Axes.set_xlabel, mocked_ax_xlabel_func)
        self.assertIs(axs.Axes.set_ylabel, mocked_ax_ylabel_func)

        # create object and call function to test
        main_sequence = createUUT()
        main_sequence._layout_ax()

        # assert correct function calls
        mocked_ax_xlim_func.assert_called_once()
        mocked_ax_ylim_func.assert_called_once()
        mocked_ax_plot_func.assert_called_once()
        self.assertEqual(2, mocked_ax_add_art_func.call_count)  # called twice
        self.assertEqual(2, mocked_ax_anno_func.call_count)  # called twice
        mocked_ax_xlabel_func.assert_called_once()
        mocked_ax_ylabel_func.assert_called_once()

    @patch('matplotlib.axes.Axes.set_xlim')
    @patch('matplotlib.axes.Axes.set_ylim')
    @patch('matplotlib.axes.Axes.plot')
    @patch('matplotlib.axes.Axes.add_artist')
    @patch('matplotlib.axes.Axes.annotate')
    @patch('matplotlib.axes.Axes.set_xlabel')
    @patch('matplotlib.axes.Axes.set_ylabel')
    def testCorrectFunctionCallArguments(self, mocked_ax_ylabel_func, mocked_ax_xlabel_func, mocked_ax_anno_func,
                                         mocked_ax_add_art_func, mocked_ax_plot_func, mocked_ax_ylim_func,
                                         mocked_ax_xlim_func):
        '''
        Test that correct functions are invoked
        '''
        # assert mocks
        self.assertIs(axs.Axes.set_xlim, mocked_ax_xlim_func)
        self.assertIs(axs.Axes.set_ylim, mocked_ax_ylim_func)
        self.assertIs(axs.Axes.plot, mocked_ax_plot_func)
        self.assertIs(axs.Axes.add_artist, mocked_ax_add_art_func)
        self.assertIs(axs.Axes.annotate, mocked_ax_anno_func)
        self.assertIs(axs.Axes.set_xlabel, mocked_ax_xlabel_func)
        self.assertIs(axs.Axes.set_ylabel, mocked_ax_ylabel_func)

        # create object and call function to test
        main_sequence = createUUT()
        main_sequence._layout_ax()

        # assert call-arguments (Axes.set_xlim)
        call_args, _ = mocked_ax_xlim_func.call_args
        self.assertEqual((0, 1), call_args[0])

        # assert call-arguments (Axes.set_ylim)
        call_args, _ = mocked_ax_ylim_func.call_args
        self.assertEqual((0, 1), call_args[0])

        # assert call-arguments (Axes.plot)
        (call_sp, call_ep), call_kwords = mocked_ax_plot_func.call_args
        self.assertEqual([0, 1], call_sp)
        self.assertEqual([1, 0], call_ep)
        self.assertEqual('x', call_kwords['marker'])
        self.assertEqual('red', call_kwords['color'])

        # assert call-arguments (Axes.add_artist) (both calls)
        expected_add_artist_calls = [mocked_ax_add_art_func(plt.Circle((0, 0), .5, alpha=.3, color='r')),
                                     mocked_ax_add_art_func(plt.Circle((1, 1), .5, alpha=.3, color='r'))]
        mocked_ax_add_art_func.has_calls(expected_add_artist_calls)

        # assert call-arguments (Axes.annotate) (both calls)
        expected_anno_calls = [mocked_ax_anno_func("Zone of Pain", xy=(.1, .2), fontsize=10),
                               mocked_ax_anno_func("Zone of Uselessness", xy=(.65, .8), fontsize=10)]
        mocked_ax_anno_func.has_calls(expected_anno_calls)

        # assert call-arguments (Axes.set_xlabel)
        call_args, call_kword = mocked_ax_xlabel_func.call_args
        self.assertEqual('[I]nstability', call_args[0])
        self.assertEqual(18, call_kword['fontsize'])

        # assert call-arguments (Axes.set_ylabel)
        call_args, call_kword = mocked_ax_ylabel_func.call_args
        self.assertEqual('[A]bstractness', call_args[0])
        self.assertEqual(18, call_kword['fontsize'])


class TestMainSequenceDefineMotionAnnotationCallback(unittest.TestCase):
    @patch('matplotlib.backend_bases.FigureCanvasBase.mpl_connect')
    @patch('matplotlib.backend_bases.FigureCanvasBase.set_window_title')
    @patch('matplotlib.text.Text.set_visible')
    @patch('matplotlib.axes.Axes.annotate')
    def testEarlyReturnIfEmptyName(self, mocked_anno_func, mocked_vis_func, mocked_set_func, mocked_con_func):
        '''
        Test that the function returns early if annotation-list is empty (no motion_event will be set)
        '''
        # assert mocks
        self.assertIs(axs.Axes.annotate, mocked_anno_func)
        self.assertIs(txt.Text.set_visible, mocked_vis_func)
        self.assertIs(bb.FigureCanvasBase.set_window_title, mocked_set_func)
        self.assertIs(bb.FigureCanvasBase.mpl_connect, mocked_con_func)

        # create mock values
        mocked_scatter = plt.gca().scatter(pd.Series(dtype=float), pd.Series(dtype=float))
        mocked_annotation_points_list = []

        # create object
        main_sequence = createUUT()
        with patch.object(main_sequence, '_annotation_points', mocked_annotation_points_list):
            with warnings.catch_warnings(record=True) as w:
                # Cause all warnings to always be triggered.
                warnings.simplefilter('always')

                # call function to test
                main_sequence._define_motion_annotation_callback(mocked_scatter)

                # assert correct setting of warning and early returning of function
                self.assertEqual([], main_sequence._annotation_points)
                self.assertEqual(len(w), 1)
                self.assertTrue('"self._names_map" is empty...returning directly, no motion_notifiy_event connected'
                                in str(w[-1].message))
                mocked_set_func.assert_called_once_with('Main Sequence')
                mocked_anno_func.assert_not_called()
                mocked_vis_func.assert_not_called()
                mocked_con_func.assert_not_called()

    @patch('matplotlib.backend_bases.FigureCanvasBase.mpl_connect')
    @patch('main_sequence.MainSequence._annotate_point')
    def testCallbackConnectionToMotionEvent(self, mocked_ms_anno_func, mocked_con_func):
        '''
        Test that the annotation-callback is correctly connected to Figure.Canvas
        '''
        # assert mock
        self.assertIs(MainSequence._annotate_point, mocked_ms_anno_func)
        self.assertIs(bb.FigureCanvasBase.mpl_connect, mocked_con_func)

        # create mock values
        mocked_scatter = plt.gca().scatter(pd.Series(dtype=float), pd.Series(dtype=float))
        mocked_annotation_points_list = [txt.Annotation('dummy-annotation1', (.5, .5), visible=False)]

        # create object
        main_sequence = createUUT()
        with patch.object(main_sequence, '_annotation_points', mocked_annotation_points_list):
            # call function to test
            main_sequence._define_motion_annotation_callback(mocked_scatter)

            # assert correct function call
            mocked_con_func.assert_called_once()

            # assert call-arguments (canvas.mpl_connect)
            (call_event, call_lambda), _ = mocked_con_func.call_args
            self.assertEqual('motion_notify_event', call_event)

            # assert correct lambda connection by invoking it
            call_lambda(None)
            mocked_ms_anno_func.assert_called_once_with(None, mocked_scatter)


class TestMainSequencePlotMetrics(unittest.TestCase):
    @patch('DataSeriesUtility.get_instability_and_abstractness_metric')
    @patch('matplotlib.axes.Axes.scatter')
    @patch('matplotlib.pyplot.show')
    @patch('main_sequence.MainSequence._define_motion_annotation_callback')
    @patch('main_sequence.MainSequence._layout_ax')
    def testCorrectFunctionCalls(self, mocked_ms_func, mocked_ms_cb_func, mocked_show_func, mocked_scatter_func,
                                 mocked_dsu_func):
        '''
        Test that functions inside this method are called correctly
        '''
        # assert mocks
        self.assertIs(dsu.get_instability_and_abstractness_metric, mocked_dsu_func)
        self.assertIs(axs.Axes.scatter, mocked_scatter_func)
        self.assertIs(plt.show, mocked_show_func)  # mock this function to no show the plotted window
        self.assertIs(MainSequence._define_motion_annotation_callback, mocked_ms_cb_func)
        self.assertIs(MainSequence._layout_ax, mocked_ms_func)

        # create return values for mocked functions
        mocked_i_metric = pd.Series(np.array([.6, .0, .1, 1., .0, .5]))
        mocked_a_metric = pd.Series(np.array([.3, 1., .0, 1., .8, .2]))
        mocked_annotation_points_list = [plt.gca().annotate(n, (x, y), visible=False) for n, x, y in
                                         zip(mocked_i_metric.index, mocked_i_metric, mocked_a_metric)]

        # assign mocked return values to mocks
        mocked_dsu_func.return_value = mocked_i_metric, mocked_a_metric
        mocked_ms_func.return_value = plt.gca()

        # create object and call function to test
        main_sequence = createUUT()
        with patch.object(main_sequence, '_annotation_points', mocked_annotation_points_list):
            main_sequence.plot_metrics()

            # assert calls (empty directory-path given for testing)
            mocked_dsu_func.assert_called_once_with('')
            mocked_ms_func.assert_called_once()
            mocked_scatter_func.assert_called_once()
            mocked_ms_cb_func.assert_called_once()
            mocked_show_func.assert_called_once()

    @patch('DataSeriesUtility.get_instability_and_abstractness_metric')
    @patch('matplotlib.axes.Axes.scatter')
    @patch('matplotlib.pyplot.show')
    @patch('main_sequence.MainSequence._define_motion_annotation_callback')
    @patch('main_sequence.MainSequence._layout_ax')
    def testCorrectFunctionCallArguments(self, mocked_ms_func, mocked_ms_cb_func, mocked_show_func, mocked_scatter_func,
                                         mocked_dsu_func):
        '''
        Test that functions inside this method are called with correct arguments
        '''
        # assert mocks
        self.assertIs(dsu.get_instability_and_abstractness_metric, mocked_dsu_func)
        self.assertIs(axs.Axes.scatter, mocked_scatter_func)
        self.assertIs(plt.show, mocked_show_func)  # mock this function to no show the plotted window
        self.assertIs(MainSequence._define_motion_annotation_callback, mocked_ms_cb_func)
        self.assertIs(MainSequence._layout_ax, mocked_ms_func)

        # create return values for mocked functions
        mocked_i_metric = pd.Series(np.array([.6, .0, .1, 1., .0, .5]))
        mocked_a_metric = pd.Series(np.array([.3, 1., .0, 1., .8, .2]))
        mocked_ax = plt.gca()
        mocked_scatter = mocked_ax.scatter(mocked_i_metric, mocked_a_metric)
        mocked_annotation_points_list = [mocked_ax.annotate(n, (x, y), visible=False) for n, x, y in
                                         zip(mocked_i_metric.index, mocked_i_metric, mocked_a_metric)]

        # assign mocked return values to mocks
        mocked_dsu_func.return_value = mocked_i_metric, mocked_a_metric
        mocked_ms_func.return_value = mocked_ax
        mocked_scatter_func.return_value = mocked_scatter

        # create object and call function to test
        main_sequence = createUUT()
        with patch.object(main_sequence, '_annotation_points', mocked_annotation_points_list):
            main_sequence.plot_metrics()

            # assert call-arguments (ax.scatter)
            (call_i_metric, call_a_metric), _ = mocked_scatter_func.call_args
            self.assertTrue(np.all(mocked_i_metric == call_i_metric))
            self.assertTrue(np.all(mocked_a_metric == call_a_metric))

            # assert call-arguments (MainSequence._define_motion_annotation_callback)
            call_args, _ = mocked_ms_cb_func.call_args
            self.assertEqual(call_args[0], mocked_scatter)


class TestMainSequenceSaveMetrics(unittest.TestCase):
    @patch('FileUtility.save_metric_to_file')
    def testCorrectFunctionCallsIfMetricsAreExisting(self, mocked_fut_save_func):
        '''
        Test that correct functions are invoked if metrics are already existing
        '''
        # assert mocks
        self.assertIs(fut.save_metric_to_file, mocked_fut_save_func)

        # create mock values
        mocked_ins_metric = pd.Series([.5], dtype=float)
        mocked_abs_metric = pd.Series([.4], dtype=float)

        # create object to test
        main_sequence = createUUT()
        with patch.object(main_sequence, '_instability_metric', mocked_ins_metric):
            with patch.object(main_sequence, '_abstractness_metric', mocked_abs_metric):
                # call function to test
                main_sequence.save_metrics('')

                # assert calls and function arguments
                call_list = [mocked_fut_save_func(mocked_ins_metric, ''),
                             mocked_fut_save_func(mocked_abs_metric, '')]
                mocked_fut_save_func.has_calls(call_list)

    @patch('DataSeriesUtility.get_instability_and_abstractness_metric')
    @patch('FileUtility.save_metric_to_file')
    def testCorrectFunctionCallsIfMetricsNotExisting(self, mocked_fut_save_func, mocked_dsu_get_func):
        '''
        Test that correct functions are invoked if metrics are not existing
        '''
        # assert mocks
        self.assertIs(fut.save_metric_to_file, mocked_fut_save_func)
        self.assertIs(dsu.get_instability_and_abstractness_metric, mocked_dsu_get_func)

        # create mock values
        mocked_ins_metric = None
        mocked_abs_metric = None
        mocked_dsu_get_func.return_value = pd.Series([.5], dtype=float), pd.Series([.4], dtype=float)

        # create object to test
        main_sequence = createUUT()
        with patch.object(main_sequence, '_instability_metric', mocked_ins_metric):
            with patch.object(main_sequence, '_abstractness_metric', mocked_abs_metric):
                # call function to test
                main_sequence.save_metrics()

                # assert calls and function arguments
                mocked_dsu_get_func.assert_called_once()
                func_calls = [mocked_fut_save_func(mocked_ins_metric, ''),
                              mocked_fut_save_func(mocked_abs_metric, '')]
                mocked_fut_save_func.has_calls(func_calls)
