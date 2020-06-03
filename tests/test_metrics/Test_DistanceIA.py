import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import unittest
from unittest.mock import patch
import sys

# make utility scripts visible
sys.path.append('scm_modules/utils/')
import DataSeriesUtility as dsu
import FileUtility as fut

sys.path.append('scm_modules/metrics/')
from distance_ia import DistanceIA


def createUUT():
    '''
    Returns an initialized object to test (no directory-path required for testing)
    '''
    return DistanceIA('')


class TestDistanceIACalculateDistance(unittest.TestCase):
    def testCorrectReturnValue(self):
        '''
        Test that the correct value is returned
        '''
        mocked_i_metric = pd.Series(np.array([.6, .0, .1, 1., .0, .5]))
        mocked_a_metric = pd.Series(np.array([.3, 1., .0, 1., .8, .2]))
        expected_calc_distance = abs(mocked_i_metric + mocked_a_metric - 1)

        # create object and call function to test
        distance_ia = createUUT()
        with patch.object(distance_ia, '_instability_metric', mocked_i_metric):
            with patch.object(distance_ia, '_abstractness_metric', mocked_a_metric):
                distance_ia._calculate_distance()

                self.assertTrue(distance_ia._distance.equals(expected_calc_distance))


class TestDistanceIAPlotDistance(unittest.TestCase):
    @patch('matplotlib.pyplot.ylabel')
    @patch('matplotlib.pyplot.xticks')
    @patch('matplotlib.pyplot.plot')
    @patch('matplotlib.pyplot.show')
    @patch('DataSeriesUtility.get_instability_and_abstractness_metric')
    @patch('distance_ia.DistanceIA._calculate_distance')
    def testCorrectFunctionCalls(self, mocked_d_func, mocked_dsu_func, mocked_show_func, mocked_plot_func,
                                 mocked_xticks_func, mocked_ylabel_func):
        '''
        Test that functions inside this method are called correctly
        '''
        # assert mocks
        self.assertIs(DistanceIA._calculate_distance, mocked_d_func)
        self.assertIs(dsu.get_instability_and_abstractness_metric, mocked_dsu_func)
        self.assertIs(plt.show, mocked_show_func)  # mock this function to no show the plotted window
        self.assertIs(plt.plot, mocked_plot_func)
        self.assertIs(plt.xticks, mocked_xticks_func)
        self.assertIs(plt.ylabel, mocked_ylabel_func)

        # create return values for mocked functions
        mocked_i_metric = pd.Series(np.array([.6, .0, .1, 1., .0, .5]))
        mocked_a_metric = pd.Series(np.array([.3, 1., .0, 1., .8, .2]))
        mocked_distance = abs(mocked_i_metric + mocked_a_metric - 1)
        mocked_dsu_func.return_value = mocked_i_metric, mocked_a_metric
        mocked_d_func.return_value = mocked_distance

        # create object and call function to test
        distance_ia = createUUT()
        with patch.object(distance_ia, '_distance', mocked_distance):
            distance_ia.plot_distance()

            # assert calls (empty directory-path given for testing)
            mocked_dsu_func.assert_called_once_with('')
            mocked_d_func.assert_called_once()
            mocked_plot_func.assert_called_once()
            mocked_xticks_func.assert_called_once()
            mocked_ylabel_func.assert_called_once()
            mocked_show_func.assert_called_once()

    @patch('matplotlib.pyplot.ylabel')
    @patch('matplotlib.pyplot.xticks')
    @patch('matplotlib.pyplot.plot')
    @patch('matplotlib.pyplot.show')
    @patch('DataSeriesUtility.get_instability_and_abstractness_metric')
    @patch('distance_ia.DistanceIA._calculate_distance')
    def testCorrectFunctionCallArguments(self, mocked_d_func, mocked_dsu_func, mocked_show_func,
                                         mocked_plot_func, mocked_xticks_func, mocked_ylabel_func):
        '''
        Test that functions inside this method are called with correct arguments
        '''
        # assert mocks
        self.assertIs(DistanceIA._calculate_distance, mocked_d_func)
        self.assertIs(dsu.get_instability_and_abstractness_metric, mocked_dsu_func)
        self.assertIs(plt.show, mocked_show_func)  # mock this function to no show the plotted window
        self.assertIs(plt.plot, mocked_plot_func)
        self.assertIs(plt.xticks, mocked_xticks_func)
        self.assertIs(plt.ylabel, mocked_ylabel_func)

        # create return values for mocked functions
        expected_i_index = ['a', 'b', 'c', 'd', 'e', 'f']
        mocked_i_metric = pd.Series(np.array([.6, .0, .1, 1., .0, .5]), index=expected_i_index)
        mocked_a_metric = pd.Series(np.array([.3, 1., .0, 1., .8, .2]))
        mocked_distance = abs(mocked_i_metric + mocked_a_metric - 1)
        mocked_dsu_func.return_value = mocked_i_metric, mocked_a_metric
        mocked_d_func.return_value = mocked_distance
        expected_ind = np.arange(mocked_distance.size)

        # create object and call function to test
        distance_ia = createUUT()
        with patch.object(distance_ia, '_distance', mocked_distance):
            distance_ia.plot_distance()

            # assert call-arguments (plt.plot)
            (call_ind, call_dist), call_kwords = mocked_plot_func.call_args
            self.assertTrue(np.all(expected_ind == call_ind))
            self.assertTrue(mocked_distance.equals(call_dist))
            self.assertEqual('x', call_kwords['marker'])
            self.assertEqual('None', call_kwords['linestyle'])

            # assert call-arguments (plt.xticks)
            (call_ind, call_i_index), call_kwords = mocked_xticks_func.call_args
            self.assertTrue(np.all(expected_ind == call_ind))
            self.assertTrue(np.all(expected_i_index == call_i_index))
            self.assertEqual(45, call_kwords['rotation'])
            self.assertEqual('right', call_kwords['ha'])

            # assert call-arguments (plt.ylabel)
            call_args, call_kwords = mocked_ylabel_func.call_args
            self.assertEqual('[D]istance', call_args[0])
            self.assertEqual(18, call_kwords['fontsize'])


class TestDistanceIASaveMetrics(unittest.TestCase):
    @patch('FileUtility.save_metric_to_file')
    def testCorrectFunctionCallsIfMetricIsExisting(self, mocked_fut_save_func):
        '''
        Test that correct functions are invoked if metric is already existing
        '''
        # assert mocks
        self.assertIs(fut.save_metric_to_file, mocked_fut_save_func)

        # create mock value
        mocked_dist_metric = pd.Series([.5], dtype=float)

        # create object to test
        distance_ia = createUUT()
        with patch.object(distance_ia, '_distance', mocked_dist_metric):
            # call function to test
            distance_ia.save_metric('')

            # assert call
            mocked_fut_save_func.assert_called_once()

    @patch('FileUtility.save_metric_to_file')
    @patch('distance_ia.DistanceIA._calculate_distance')
    def testCorrectFunctionCallsIfMetricNotExisting(self, mocked_d_calc_func, mocked_fut_save_func):
        '''
        Test that correct functions are invoked if metrics is not existing
        '''
        # assert mocks
        self.assertIs(DistanceIA._calculate_distance, mocked_d_calc_func)
        self.assertIs(fut.save_metric_to_file, mocked_fut_save_func)

        # create mock values
        mocked_dist_metric = None
        mocked_d_calc_func.return_value = pd.Series([.5], dtype=float)

        # create object to test
        distance_ia = createUUT()
        with patch.object(distance_ia, '_distance', mocked_dist_metric):
            # call function to test
            distance_ia.save_metric()

            # assert calls and function arguments
            mocked_d_calc_func.assert_called_once()
            mocked_fut_save_func.assert_called_once()
