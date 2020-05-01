import numpy as np
import pandas as pd
import unittest
from unittest.mock import patch
import sys

sys.path.append('utils/')
import DataSeriesUtility as dsu

sys.path.append('metrics/')
from instability_metric import InstabilityMetric
from abstractness_metric import AbstractnessMetric


class TestDataSeriesUtilityGetInstabilityAndAbstractnessMetric(unittest.TestCase):
    def testEmtpyFilePath(self):
        '''
        Test that an empty directory path does still result in two pd.Series types with dtype=float
        '''
        returned_instability_metric, returned_abstractness_metric = dsu.get_instability_and_abstractness_metric('')
        self.assertIsInstance(returned_instability_metric, type(pd.Series(dtype=float)))
        self.assertIsInstance(returned_abstractness_metric, type(pd.Series(dtype=float)))
        self.assertEqual(returned_instability_metric.dtype, float)
        self.assertEqual(returned_abstractness_metric.dtype, float)

    @patch('DataSeriesUtility.reorder_data_series_elements')
    @patch('DataSeriesUtility.pad_data_series_with_default_values')
    @patch('abstractness_metric.AbstractnessMetric.compute_abstractness')
    @patch('instability_metric.InstabilityMetric.compute_instability')
    def testCorrectFunctionCallsWithEmptyFilePath(self, mocked_comp_i_func, mocked_comp_a_func,
                                                  mocked_pad_func, mocked_reorder_func):
        '''
        Test that the correct functions are invoked (or not invoked) when an empty filepath was provided
        '''
        # assert mocks
        self.assertIs(InstabilityMetric.compute_instability, mocked_comp_i_func)
        self.assertIs(AbstractnessMetric.compute_abstractness, mocked_comp_a_func)
        self.assertIs(dsu.reorder_data_series_elements, mocked_reorder_func)

        # call function to test
        returned_i_metric, returned_a_metric = dsu.get_instability_and_abstractness_metric('')
        mocked_comp_i_func.assert_called_once()
        mocked_comp_a_func.assert_called_once()
        mocked_pad_func.assert_not_called()
        mocked_reorder_func.assert_called_once()

    @patch('DataSeriesUtility.reorder_data_series_elements')
    @patch('DataSeriesUtility.pad_data_series_with_default_values')
    @patch('abstractness_metric.AbstractnessMetric.compute_abstractness')
    @patch('instability_metric.InstabilityMetric.compute_instability')
    def testCorrectFunctionCallsWithCorrectFilePath(self, mocked_comp_i_func, mocked_comp_a_func,
                                                    mocked_pad_func, mocked_reorder_func):
        '''
        Test that the correct functions are invoked when A and I of different size are returned by compute_X function
        '''
        # assert mocks
        self.assertIs(InstabilityMetric.compute_instability, mocked_comp_i_func)
        self.assertIs(AbstractnessMetric.compute_abstractness, mocked_comp_a_func)
        self.assertIs(dsu.pad_data_series_with_default_values, mocked_pad_func)
        self.assertIs(dsu.reorder_data_series_elements, mocked_reorder_func)

        # set return values of mocked functions
        data_series = pd.Series(np.ones(5), dtype=float)
        data_series_to_pad = pd.Series(np.ones(3), dtype=float)
        padded_data_series = pd.Series([1, 1, 1, 0, 0], dtype=float)
        mocked_comp_i_func.return_value = data_series
        mocked_comp_a_func.return_value = data_series_to_pad
        mocked_pad_func.return_value = padded_data_series

        # call function to test
        returned_i_metric, returned_a_metric = dsu.get_instability_and_abstractness_metric('')
        mocked_comp_i_func.assert_called_once()
        mocked_comp_a_func.assert_called_once()
        mocked_pad_func.assert_called_once_with(data_series, data_series_to_pad)
        mocked_reorder_func.assert_called_once_with(data_series, padded_data_series)


class TestDataSeriesUtilityPadDataSeriesWithDefaultValues(unittest.TestCase):
    def testEmtpyFunctionArguments(self):
        '''
        Test that if either first or second argument are not of type pd.Series an empty pd.Series
        with dtype=float is returned
        '''
        empty_data_series = pd.Series(dtype=float)
        # first arg empty
        returned_padded_data_series = dsu.pad_data_series_with_default_values(None, empty_data_series)
        self.assertIsInstance(returned_padded_data_series, type(pd.Series(dtype=float)))
        self.assertEqual(returned_padded_data_series.dtype, float)
        # second arg empty
        returned_padded_data_series = dsu.pad_data_series_with_default_values(empty_data_series, None)
        self.assertIsInstance(returned_padded_data_series, type(pd.Series(dtype=float)))
        self.assertEqual(returned_padded_data_series.dtype, float)

    def testCorrectPadding(self):
        '''
        Test that
            - the second argument is correctly padded with a default value
            - all indices are present in padded array
        '''
        data_series = pd.Series(np.ones(5), index=['a', 'b', 'c', 'd', 'e'], dtype=float)
        data_series_to_pad = pd.Series(np.ones(2), index=['c', 'e'], dtype=float)
        returned_padded_data_series = dsu.pad_data_series_with_default_values(data_series, data_series_to_pad)
        self.assertEqual(returned_padded_data_series.size, data_series.size)
        for index in returned_padded_data_series.index:
            self.assertTrue(index in data_series.index)
        self.assertEqual(returned_padded_data_series[3], dsu.DEFAULT_PADDING_VALUE)


class TestReorderDataSeriesElements(unittest.TestCase):
    def testEmtpyFunctionArguments(self):
        '''
        Test that if either first or second argument are not of type pd.Series an empty pd.Series
        with dtype=float is returned
        '''
        empty_data_series = pd.Series(dtype=float)
        # first arg empty
        returned_reorderd_data_series = dsu.reorder_data_series_elements(None, empty_data_series)
        self.assertIsInstance(returned_reorderd_data_series, type(pd.Series(dtype=float)))
        self.assertEqual(returned_reorderd_data_series.dtype, float)
        # second arg empty
        returned_reorderd_data_series = dsu.pad_data_series_with_default_values(empty_data_series, None)
        self.assertIsInstance(returned_reorderd_data_series, type(pd.Series(dtype=float)))
        self.assertEqual(returned_reorderd_data_series.dtype, float)

    def testCorrectReordering(self):
        '''
        Test that the seconds argument is correctly reordered
        '''
        data_series = pd.Series(np.ones(5), index=['a', 'b', 'c', 'd', 'e'], dtype=float)
        data_series_to_reorder = pd.Series(np.ones(5), index=['c', 'e', 'a', 'b', 'd'], dtype=float)
        returned_reorderd_data_series = dsu.reorder_data_series_elements(data_series, data_series_to_reorder)
        self.assertEqual(returned_reorderd_data_series.size, data_series.size)
        for index in returned_reorderd_data_series.index:
            self.assertEqual(returned_reorderd_data_series[index], data_series[index])
