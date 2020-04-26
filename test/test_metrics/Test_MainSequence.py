import matplotlib.pyplot as plt
import matplotlib.axes as axs
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


class TestMainSequencePlotMetrics(unittest.TestCase):
    @patch('DataSeriesUtility.get_instability_and_abstractness_metric')
    @patch('matplotlib.axes.Axes.scatter')
    @patch('matplotlib.pyplot.show')
    @patch('main_sequence.MainSequence._define_motion_annotation_callback')
    @patch('main_sequence.MainSequence._layout_ax')
    def testEmptyNamesList(self, mocked_ms_func, mocked_ms_cb_func, mocked_show_func, mocked_scatter_func,
    mocked_dsu_func):
        '''
        Test that function returns if MainSequence._names_map is empty
        '''
        # assert mocks
        self.assertIs(dsu.get_instability_and_abstractness_metric, mocked_dsu_func)
        self.assertIs(axs.Axes.scatter, mocked_scatter_func)
        self.assertIs(plt.show, mocked_show_func) # mock this function to no show the plotted window
        self.assertIs(MainSequence._define_motion_annotation_callback, mocked_ms_cb_func)
        self.assertIs(MainSequence._layout_ax, mocked_ms_func)
        
        # use empty data frames to create empty names-map
        mocked_dsu_func.return_value = pd.DataFrame(), pd.DataFrame()
        

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")

            # create object and call function to test
            main_sequence = createUUT()
            main_sequence.plot_metrics()

            # assert correct result (no further function calls)
            mocked_ms_func.assert_not_called()
            mocked_scatter_func.assert_not_called()
            mocked_ms_cb_func.assert_not_called()
            mocked_show_func.assert_not_called()
            self.assertEqual(len(w), 1)
            self.assertTrue('"self._names_map" is empty...returning directly' in str(w[-1].message))
        

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
        mocked_dsu_func.return_value = mocked_i_metric, mocked_a_metric
        mocked_ms_func.return_value = plt.gca()
        mocked_names_map = [(n, (x, y)) for n, x, y in zip(mocked_i_metric.index, mocked_i_metric, mocked_a_metric)]
        
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

# run TestSuite
unittest.TextTestRunner(verbosity=2).run(suite)
