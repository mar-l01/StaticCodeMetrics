import matplotlib.axes as axs
import matplotlib.backend_bases as bb
import matplotlib.backends.backend_tkagg as btk
import matplotlib.collections as coll
import matplotlib.pyplot as plt
import matplotlib.text as txt
import numpy as np
import pandas as pd
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
import sys
import warnings

# make utility scripts visible
sys.path.append('utils/')
import DataSeriesUtility as dsu

sys.path.append('metrics/')
from main_sequence import MainSequence


def createUUT():
    '''
    Returns an initialized object to test (no directory-path required for testing)
    '''
    return MainSequence('')


class TestMainSequenceAnnotatePoint(unittest.TestCase):
    @patch('matplotlib.collections.PathCollection.contains')
    @patch('matplotlib.axes.Axes.annotate')
    @patch('matplotlib.text.Text.set_visible')
    @patch('matplotlib.backends.backend_tkagg.FigureCanvasTkAgg.draw_idle')
    def testCorrectFunctionCallsIfPointSelected(self, mocked_fig_draw_func, mocked_txt_vis_func, mocked_ax_anno_func,
    mocked_coll_cont_func):
        '''
        Test correct function calls if point is contained in scattered point
        '''
        # assert mocks
        self.assertIs(btk.FigureCanvasTkAgg.draw_idle, mocked_fig_draw_func)
        self.assertIs(txt.Text.set_visible, mocked_txt_vis_func)
        self.assertIs(axs.Axes.annotate, mocked_ax_anno_func)
        self.assertIs(coll.PathCollection.contains, mocked_coll_cont_func)
        
        # create mock values
        mocked_ax = plt.gca()
        mocked_ax.set_xlim((0,1))
        mocked_ax.set_ylim((0,1))
        mocked_scatter = mocked_ax.scatter(pd.Series([.5], dtype=float), pd.Series([.5], dtype=float))   
        mocked_coll_cont_func.return_value = True, {'ind': np.array([0], dtype=int)}        
        mocked_names_map = [('test-annotation', (.5, .5))]
        mocked_mouse_event = bb.MouseEvent('mocked-mouse-event', plt.gcf().canvas, 322, 242) # (322, 242) := on point(.5|.5)
        mocked_annotated_point = txt.Annotation('dummy-annotation', (.5, .5))
        mocked_annotated_point.set_visible(False)

        # create object
        main_sequence = createUUT()
        with patch.object(main_sequence, '_annotated_point', mocked_annotated_point):
            with patch.object(main_sequence, '_names_map', mocked_names_map):
                with patch.object(mocked_mouse_event, 'inaxes', mocked_ax):
                    # call function to test
                    main_sequence._annotate_point(mocked_mouse_event, mocked_ax, mocked_scatter)

                    # assert function calls
                    mocked_coll_cont_func.assert_called_once()
                    mocked_ax_anno_func.assert_called_once()
                    mocked_txt_vis_func.assert_called() # called several times
                    mocked_fig_draw_func.assert_called_once()

    @patch('matplotlib.collections.PathCollection.contains')
    @patch('matplotlib.text.Text.set_visible')
    @patch('matplotlib.text.Text.get_visible')
    @patch('matplotlib.backends.backend_tkagg.FigureCanvasTkAgg.draw_idle')
    def testCorrectFunctionCallsIfPointNotSelected(self, mocked_fig_draw_func, mocked_txt_get_vis_func, mocked_txt_set_vis_func,
    mocked_coll_cont_func):
        '''
        Test correct function calls if point is not contained in any scattered point but in axes-view
        '''
        # assert mocks
        self.assertIs(btk.FigureCanvasTkAgg.draw_idle, mocked_fig_draw_func)
        self.assertIs(txt.Text.get_visible, mocked_txt_get_vis_func)
        self.assertIs(txt.Text.set_visible, mocked_txt_set_vis_func)
        self.assertIs(coll.PathCollection.contains, mocked_coll_cont_func)
        
        # create mock values
        mocked_ax = plt.gca()
        mocked_ax.set_xlim((0,1))
        mocked_ax.set_ylim((0,1))
        mocked_scatter = mocked_ax.scatter(pd.Series([.5], dtype=float), pd.Series([.5], dtype=float))   
        mocked_plt_fig_func = MagicMock('plt.gcf', return_value=plt.gcf()) # mock using gcf() for scatter-plot 
        mocked_coll_cont_func.return_value = False, {}        
        mocked_mouse_event = bb.MouseEvent('mocked-mouse-event', plt.gcf().canvas, 100, 200) # (100, 200) := not on point(.5|.5)
        mocked_annotated_point = txt.Annotation('dummy-annotation', (.5, .5))
        mocked_txt_get_vis_func.return_value = True

        # create object
        main_sequence = createUUT()
        with patch.object(main_sequence, '_annotated_point', mocked_annotated_point):
            with patch.object(mocked_mouse_event, 'inaxes', mocked_ax):
                # call function to test
                main_sequence._annotate_point(mocked_mouse_event, mocked_ax, mocked_scatter)

                # assert function calls
                mocked_coll_cont_func.assert_called_once()
                mocked_txt_get_vis_func.assert_called() # called several times
                mocked_txt_set_vis_func.assert_called() # called several times
                mocked_fig_draw_func.assert_called_once()


class TestMainSequenceLayoutAx(unittest.TestCase):
    @patch('matplotlib.axes.Axes.set_xlim')
    @patch('matplotlib.axes.Axes.set_ylim')
    @patch('matplotlib.axes.Axes.plot')
    @patch('matplotlib.axes.Axes.add_artist')
    @patch('matplotlib.axes.Axes.annotate')
    @patch('matplotlib.axes.Axes.set_xlabel')
    @patch('matplotlib.axes.Axes.set_ylabel')
    def testCorrectFunctionCalls(self, mocked_ax_ylabel_func, mocked_ax_xlabel_func, mocked_ax_anno_func, mocked_ax_add_art_func,
    mocked_ax_plot_func, mocked_ax_ylim_func, mocked_ax_xlim_func):
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
        returned_ax = main_sequence._layout_ax()
        
        # assert correct function calls        
        mocked_ax_xlim_func.assert_called_once()
        mocked_ax_ylim_func.assert_called_once()
        mocked_ax_plot_func.assert_called_once()
        self.assertEqual(2, mocked_ax_add_art_func.call_count) # called twice
        self.assertEqual(2, mocked_ax_anno_func.call_count) # called twice
        mocked_ax_xlabel_func.assert_called_once()
        mocked_ax_ylabel_func.assert_called_once()

    @patch('matplotlib.axes.Axes.set_xlim')
    @patch('matplotlib.axes.Axes.set_ylim')
    @patch('matplotlib.axes.Axes.plot')
    @patch('matplotlib.axes.Axes.add_artist')
    @patch('matplotlib.axes.Axes.annotate')
    @patch('matplotlib.axes.Axes.set_xlabel')
    @patch('matplotlib.axes.Axes.set_ylabel')
    def testCorrectFunctionCallArguments(self, mocked_ax_ylabel_func, mocked_ax_xlabel_func, mocked_ax_anno_func, mocked_ax_add_art_func,
    mocked_ax_plot_func, mocked_ax_ylim_func, mocked_ax_xlim_func):
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
        returned_ax = main_sequence._layout_ax()
        
        # assert call-arguments (Axes.set_xlim)
        call_args, _ = mocked_ax_xlim_func.call_args
        self.assertEqual((0,1), call_args[0])
        
        # assert call-arguments (Axes.set_ylim)
        call_args, _ = mocked_ax_ylim_func.call_args
        self.assertEqual((0,1), call_args[0])
        
        # assert call-arguments (Axes.plot)
        (call_sp, call_ep), call_kwords = mocked_ax_plot_func.call_args
        self.assertEqual([0,1], call_sp)
        self.assertEqual([1,0], call_ep)
        self.assertEqual('x', call_kwords['marker'])
        self.assertEqual('red', call_kwords['color'])
        
        # assert call-arguments (Axes.add_artist) (both calls)
        expected_add_artist_calls = [mocked_ax_add_art_func(plt.Circle((0, 0), .5, alpha=.3, color='r')), mocked_ax_add_art_func(plt.Circle((1, 1), .5, alpha=.3, color='r'))]
        mocked_ax_add_art_func.has_calls(expected_add_artist_calls)
        
        # assert call-arguments (Axes.annotate) (both calls)
        expected_anno_calls = [mocked_ax_anno_func("Zone of Pain", xy=(.1, .2), fontsize=10), mocked_ax_anno_func("Zone of Uselessness", xy=(.65, .8), fontsize=10)]
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
    def testInitialSettingOfAnnotationPoint(self):
        '''
        Test that the annotation point is set initally and invisible
        '''
        # create mock values
        mocked_ax = plt.gca()
        mocked_scatter = mocked_ax.scatter(pd.Series(dtype=float), pd.Series(dtype=float))
        mocked_names_map = [('test-annotation', (0, 1))] # one element enough to test initial setting (:= [0])
        expected_annotated_point = mocked_ax.annotate(*mocked_names_map[0])

        # create object
        main_sequence = createUUT()
        with patch.object(main_sequence, '_names_map', mocked_names_map):
            # call function to test
            main_sequence._define_motion_annotation_callback(mocked_ax, mocked_scatter)

            # assert correct setting of annotation point
            self.assertEqual(expected_annotated_point.xy, main_sequence._annotated_point.xy)
            self.assertEqual(expected_annotated_point.get_text(), main_sequence._annotated_point.get_text())
            self.assertFalse(main_sequence._annotated_point.get_visible())

    @patch('matplotlib.backend_bases.FigureCanvasBase.mpl_connect')
    @patch('matplotlib.backend_bases.FigureCanvasBase.set_window_title')
    @patch('matplotlib.text.Text.set_visible')
    @patch('matplotlib.axes.Axes.annotate')
    def testEarlyReturnIfEmptyName(self, mocked_anno_func, mocked_vis_func, mocked_set_func, mocked_con_func):
        '''
        Test that the function returns early if names-map is empty (no motion_event will be set)
        '''
        # assert mocks
        self.assertIs(axs.Axes.annotate, mocked_anno_func)
        self.assertIs(txt.Text.set_visible, mocked_vis_func)
        self.assertIs(bb.FigureCanvasBase.set_window_title, mocked_set_func)
        self.assertIs(bb.FigureCanvasBase.mpl_connect, mocked_con_func)

        # create mock values
        mocked_ax = plt.gca()
        mocked_scatter = mocked_ax.scatter(pd.Series(dtype=float), pd.Series(dtype=float))
        mocked_names_map = [] # empty names-map

        # create object
        main_sequence = createUUT()
        with patch.object(main_sequence, '_names_map', mocked_names_map):
            with warnings.catch_warnings(record=True) as w:
                # Cause all warnings to always be triggered.
                warnings.simplefilter('always')

                # call function to test
                main_sequence._define_motion_annotation_callback(mocked_ax, mocked_scatter)

                # assert correct setting of warning and early returning of function
                self.assertEqual(None, main_sequence._annotated_point)
                self.assertEqual(len(w), 1)
                self.assertTrue('"self._names_map" is empty...returning directly, no motion_notifiy_event connected' in str(w[-1].message))
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
        mocked_ax = plt.gca()
        mocked_scatter = mocked_ax.scatter(pd.Series(dtype=float), pd.Series(dtype=float))
        mocked_names_map = [('test-annotation', (0, 1))]

        # create object
        main_sequence = createUUT()
        with patch.object(main_sequence, '_names_map', mocked_names_map):
            # call function to test
            main_sequence._define_motion_annotation_callback(mocked_ax, mocked_scatter)

            # assert correct function call
            mocked_con_func.assert_called_once()

            # assert call-arguments (canvas.mpl_connect)
            (call_event, call_lambda), _ = mocked_con_func.call_args
            self.assertEqual('motion_notify_event', call_event)

            # assert correct lambda connection by invoking it
            call_lambda(None)
            mocked_ms_anno_func.assert_called_once_with(None, mocked_ax, mocked_scatter)


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
        self.assertIs(plt.show, mocked_show_func) # mock this function to no show the plotted window
        self.assertIs(MainSequence._define_motion_annotation_callback, mocked_ms_cb_func)
        self.assertIs(MainSequence._layout_ax, mocked_ms_func)

        # create return values for mocked functions
        mocked_i_metric = pd.Series(np.array([.6, .0, .1, 1., .0, .5]))
        mocked_a_metric = pd.Series(np.array([.3, 1., .0, 1., .8, .2]))
        mocked_names_map = [(n, (x, y)) for n, x, y in zip(mocked_i_metric.index, mocked_i_metric, mocked_a_metric)]

        # assign mocked return values to mocks
        mocked_dsu_func.return_value = mocked_i_metric, mocked_a_metric
        mocked_ms_func.return_value = plt.gca()

        # create object and call function to test
        main_sequence = createUUT()
        with patch.object(main_sequence, '_names_map', mocked_names_map):
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
        self.assertIs(plt.show, mocked_show_func) # mock this function to no show the plotted window
        self.assertIs(MainSequence._define_motion_annotation_callback, mocked_ms_cb_func)
        self.assertIs(MainSequence._layout_ax, mocked_ms_func)

        # create return values for mocked functions
        mocked_i_metric = pd.Series(np.array([.6, .0, .1, 1., .0, .5]))
        mocked_a_metric = pd.Series(np.array([.3, 1., .0, 1., .8, .2]))
        mocked_ax = plt.gca()
        mocked_scatter = mocked_ax.scatter(mocked_i_metric, mocked_a_metric)
        mocked_names_map = [(n, (x, y)) for n, x, y in zip(mocked_i_metric.index, mocked_i_metric, mocked_a_metric)]

        # assign mocked return values to mocks
        mocked_dsu_func.return_value = mocked_i_metric, mocked_a_metric
        mocked_ms_func.return_value = mocked_ax
        mocked_scatter_func.return_value = mocked_scatter

        # create object and call function to test
        main_sequence = createUUT()
        with patch.object(main_sequence, '_names_map', mocked_names_map):
            main_sequence.plot_metrics()

            # assert call-arguments (ax.scatter)
            (call_i_metric, call_a_metric), _ = mocked_scatter_func.call_args
            self.assertTrue(np.all(mocked_i_metric == call_i_metric))
            self.assertTrue(np.all(mocked_a_metric == call_a_metric))

            # assert call-arguments (MainSequence._define_motion_annotation_callback)
            (call_ax, call_sc), _ = mocked_ms_cb_func.call_args
            self.assertEqual(mocked_ax, call_ax)
            self.assertEqual(mocked_scatter, call_sc)


# create TestSuite with above TestCases
suite = unittest.TestSuite()
suite.addTests(unittest.makeSuite(TestMainSequenceAnnotatePoint))
suite.addTests(unittest.makeSuite(TestMainSequenceLayoutAx))
suite.addTests(unittest.makeSuite(TestMainSequenceDefineMotionAnnotationCallback))
suite.addTests(unittest.makeSuite(TestMainSequencePlotMetrics))

# run TestSuite
unittest.TextTestRunner(verbosity=2).run(suite)
