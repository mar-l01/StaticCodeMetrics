import matplotlib.axes as axs
import matplotlib.backend_bases as bb
import matplotlib.pyplot as plt
import matplotlib.text as txt
import numpy as np
import pandas as pd
import unittest
from unittest.mock import patch
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
    @patch('matplotlib.text.Annotation.set_visible')
    @patch('matplotlib.axes.Axes.annotate')
    def testEarlyReturnIfEmptyName(self, mocked_anno_func, mocked_vis_func, mocked_set_func, mocked_con_func):
        '''
        Test that the function returns early if names-map is empty (no motion_event will be set)
        '''
        # assert mocks
        self.assertIs(axs.Axes.annotate, mocked_anno_func)
        self.assertIs(txt.Annotation.set_visible, mocked_vis_func)
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
suite.addTests(unittest.makeSuite(TestMainSequencePlotMetrics))
suite.addTests(unittest.makeSuite(TestMainSequenceDefineMotionAnnotationCallback))

# run TestSuite
unittest.TextTestRunner(verbosity=2).run(suite)
