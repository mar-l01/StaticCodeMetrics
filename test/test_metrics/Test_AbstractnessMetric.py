import os
import pandas as pd
import unittest
from unittest.mock import patch
import sys
import warnings

sys.path.append('utils/')
import FileUtility as fut

sys.path.append('metrics/')
from abstractness_metric import AbstractnessMetric
from abstractness_metric import ALLOWED_FILE_EXTENSIONS

# constants
TEST_CODE_FILES = 'test/files/abstractness_metric_test_files/'
ABSTRACT_CLASS_FILE = TEST_CODE_FILES + 'abstract_class.h'
NON_ABSTRACT_CLASS_FILE = TEST_CODE_FILES + 'non_abstract_class.h'


def createUUT(dir_path=''):
    '''
    Returns an initialized object to test
    '''
    return AbstractnessMetric(dir_path)


class TestAbstractnessMetricGetNumberOfInterfacesAndClassesOfFile(unittest.TestCase):
    def testEmptyFilePath(self):
        '''
        Test that a valid result is returned although an empty filepath is provided
        '''
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")

            # create object and call function to test
            abstractness_metric = createUUT()
            returned_nb_interfaces, returned_nb_classes = abstractness_metric._get_number_of_interfaces_and_classes_of_file('')

            # assert correct result
            self.assertEqual(returned_nb_interfaces, 0)
            self.assertEqual(returned_nb_classes, 0)
            self.assertEqual(len(w), 1)
            self.assertTrue('...returning default values' in str(w[-1].message))

    def testAbstractClassFile(self):
        '''
        Test that an abstract class is recognized successfully
        '''
        # create object and call function to test
        abstractness_metric = createUUT()
        returned_nb_interfaces, returned_nb_classes = \
            abstractness_metric._get_number_of_interfaces_and_classes_of_file(ABSTRACT_CLASS_FILE)

        # assert correct result
        self.assertEqual(returned_nb_interfaces, 1)
        self.assertEqual(returned_nb_classes, 1)

    def testNonAbstractClassFile(self):
        '''
        Test that no abstract class is found
        '''
        # create object and call function to test
        abstractness_metric = createUUT()
        returned_nb_interfaces, returned_nb_classes = \
            abstractness_metric._get_number_of_interfaces_and_classes_of_file(NON_ABSTRACT_CLASS_FILE)

        # assert correct result
        self.assertEqual(returned_nb_interfaces, 0)
        self.assertEqual(returned_nb_classes, 1)


class TestAbstractnessMetricSearchFilesForInterfaces(unittest.TestCase):
    @patch('abstractness_metric.AbstractnessMetric._get_number_of_interfaces_and_classes_of_file')
    def testCorrectNumberOfFunctionCalls(self, mocked_a_get_func):
        '''
        Test that mocked function is called as often as files are present in the given directory
        '''
        # assert mocks
        self.assertIs(AbstractnessMetric._get_number_of_interfaces_and_classes_of_file, mocked_a_get_func)

        # set dummy return values of mocked function
        mocked_a_get_func.return_value = 0, 1

        # create object and call function to test
        abstractness_metric = createUUT(TEST_CODE_FILES)
        with patch.object(abstractness_metric, '_list_of_files', os.listdir(TEST_CODE_FILES)):
            abstractness_metric._search_files_for_interfaces()

            # assert that function was called 2 times
            expected_nb_method_calls = len(os.listdir(TEST_CODE_FILES))
            self.assertEqual(mocked_a_get_func.call_count, expected_nb_method_calls)

    @patch('abstractness_metric.AbstractnessMetric._get_number_of_interfaces_and_classes_of_file')
    @patch('FileUtility.extract_filename')
    def testCorrectSettingOfCellsInMatrix(self, mocked_fut_func, mocked_a_get_func):
        '''
        Test that a correct cell is set in the member-matrix
        '''
        # assert mocks
        self.assertIs(fut.extract_filename, mocked_fut_func)
        self.assertIs(AbstractnessMetric._get_number_of_interfaces_and_classes_of_file, mocked_a_get_func)

        # set dummy return values of mocked function
        mocked_fut_func.side_effect = ['row1', 'row2']
        mocked_a_get_func.side_effect = [(0, 1), (2, 3)]

        # create object and call function to test
        abstractness_metric = createUUT(TEST_CODE_FILES)
        with patch.object(abstractness_metric, '_list_of_files', os.listdir(TEST_CODE_FILES)):
            abstractness_metric._search_files_for_interfaces()

            # assert correct setting of matrix
            self.assertEqual(abstractness_metric._interface_class_matrix['row1']['N_a'], 0)
            self.assertEqual(abstractness_metric._interface_class_matrix['row1']['N_c'], 1)
            self.assertEqual(abstractness_metric._interface_class_matrix['row2']['N_a'], 2)
            self.assertEqual(abstractness_metric._interface_class_matrix['row2']['N_c'], 3)


class TestAbstractnessMetricCalculateAbstractnessForEachFile(unittest.TestCase):
    def testCorrectCalculation(self):
        '''
        Test that a the abstractness metric is computed correctly
        '''
        # create matrix mock
        matrix_mock = pd.DataFrame(index=['N_a', 'N_c'], dtype=int)
        matrix_mock['row1'] = [1, 1]
        matrix_mock['row2'] = [2, 3]
        matrix_mock['row3'] = [0, 0]

        # create object and call function to test
        abstractness_metric = createUUT()
        with patch.object(abstractness_metric, '_interface_class_matrix', matrix_mock):
            returned_matrix = abstractness_metric._calculate_abstractness_for_each_file()

            # assert correct computation of abstractness metric
            self.assertEqual(returned_matrix['row1'], 1)
            self.assertEqual(returned_matrix['row2'], (2/3))
            self.assertEqual(returned_matrix['row3'], 0)


class TestAbstractnessMetricComputeAbstractness(unittest.TestCase):
    @patch('FileUtility.get_all_code_files')
    @patch('abstractness_metric.AbstractnessMetric._search_files_for_interfaces')
    @patch('abstractness_metric.AbstractnessMetric._calculate_abstractness_for_each_file')
    def testCorrectFunctionCallsWithEmptyFilePath(self, mocked_a_calc_func, mocked_a_search_func, mocked_fut_get_func):
        '''
        Test that the correct functions are invoked when an empty filepath was provided
        '''
        # assert mocks
        self.assertIs(AbstractnessMetric._calculate_abstractness_for_each_file, mocked_a_calc_func)
        self.assertIs(AbstractnessMetric._search_files_for_interfaces, mocked_a_search_func)
        self.assertIs(fut.get_all_code_files, mocked_fut_get_func)

        # create object and call function to test
        abstractness_metric = createUUT()
        abstractness_metric.compute_abstractness()

        # assert function calls
        mocked_fut_get_func.assert_called_once()
        mocked_a_search_func.assert_called_once()
        mocked_a_calc_func.assert_called_once()

    @patch('FileUtility.get_all_code_files')
    @patch('abstractness_metric.AbstractnessMetric._search_files_for_interfaces')
    @patch('abstractness_metric.AbstractnessMetric._calculate_abstractness_for_each_file')
    def testCorrectFunctionCallsWithNonEmptyFilePath(self, mocked_a_calc_func, mocked_a_search_func, mocked_fut_get_func):
        '''
        Test that the correct functions are invoked when a non-empty filepath was provided
        '''
        # assert mocks
        self.assertIs(AbstractnessMetric._calculate_abstractness_for_each_file, mocked_a_calc_func)
        self.assertIs(AbstractnessMetric._search_files_for_interfaces, mocked_a_search_func)
        self.assertIs(fut.get_all_code_files, mocked_fut_get_func)

        # create object and call function to test
        abstractness_metric = createUUT(TEST_CODE_FILES)
        abstractness_metric.compute_abstractness()

        # assert function calls
        mocked_fut_get_func.assert_called_once_with(TEST_CODE_FILES, ALLOWED_FILE_EXTENSIONS)
        mocked_a_search_func.assert_called_once()
        mocked_a_calc_func.assert_called_once()
