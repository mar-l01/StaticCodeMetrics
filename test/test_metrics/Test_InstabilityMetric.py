import numpy as np
import os
import pandas as pd
import unittest
from unittest.mock import patch
import sys
import warnings

sys.path.append('utils/')
import FileUtility as fut

sys.path.append('metrics/')
from instability_metric import InstabilityMetric
from instability_metric import ALLOWED_FILE_EXTENSIONS

# constants
TEST_CODE_FILES = 'test/files/instability_metric_test_files/'
STD_LIB_INCLUDE_FILE = TEST_CODE_FILES + 'lib1.hpp'
USER_LIB_INCLUDE_FILE = TEST_CODE_FILES + 'lib2.hpp'
SOURCE_FILE = TEST_CODE_FILES + 'source.cpp'


def createUUT(dir_path=''):
    '''
    Returns an initialized object to test
    '''
    return InstabilityMetric(dir_path)


class TestInstabilityMetricGetIncludesOfFile(unittest.TestCase):
    def testEmptyFilePath(self):
        '''
        Test that a valid result is returned although an empty filepath is provided
        '''
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")

            # create object and call function to test
            instability_metric = createUUT()
            returned_user_include_list, returned_stl_include_list = instability_metric._get_includes_of_file('')

            # assert correct result
            self.assertEqual(returned_user_include_list, [])
            self.assertEqual(returned_stl_include_list, [])
            self.assertEqual(len(w), 1)
            self.assertTrue('...returning default values' in str(w[-1].message))

    def testStdLibInclude(self):
        '''
        Test that a standard-library include is recognized correctly (denoted with #include <...>)
        '''
        # create object and call function to test
        instability_metric = createUUT()
        returned_user_include_list, returned_stl_include_list = instability_metric._get_includes_of_file(STD_LIB_INCLUDE_FILE)

        # assert correct result
        self.assertEqual(len(returned_user_include_list), 0)
        self.assertEqual(len(returned_stl_include_list), 1)

    def testUserLibInclude(self):
        '''
        Test that an user-library include is recognized correctly (denoted with #include "...")
        '''
        # create object and call function to test
        instability_metric = createUUT()
        returned_user_include_list, returned_stl_include_list = instability_metric._get_includes_of_file(USER_LIB_INCLUDE_FILE)

        # assert correct result
        self.assertEqual(len(returned_user_include_list), 1)
        self.assertEqual(len(returned_stl_include_list), 0)

    def testUserLibAndStdLibInclude(self):
        '''
        Test that an user-library include and a std-include are recognized correctly
        '''
        # create object and call function to test
        instability_metric = createUUT()
        returned_user_include_list, returned_stl_include_list = instability_metric._get_includes_of_file(SOURCE_FILE)

        # assert correct result
        self.assertEqual(len(returned_user_include_list), 2)
        self.assertEqual(len(returned_stl_include_list), 1)


class TestInstabilityMetricCreateUserIncludeMatrix(unittest.TestCase):
    @patch('FileUtility.extract_filename')
    def testCorrectSizeOfMatrix(self, mocked_fut_func):
        '''
        Test that the size of the returned matrix is correct
        '''
        # assert mock
        self.assertIs(fut.extract_filename, mocked_fut_func)

        # define dummy return value
        mocked_fut_func.return_value = "test"

        # create object and call function to test
        instability_metric = createUUT(TEST_CODE_FILES)
        with patch.object(instability_metric, '_list_of_user_files', os.listdir(TEST_CODE_FILES)):
            instability_metric._create_user_include_matrix()

            # assert correct size of matrix
            self.assertEqual(instability_metric._include_matrix.shape, instability_metric._include_matrix.shape)

    @patch('FileUtility.extract_filename')
    def testCorrectIndexAndColumnLabelsOfMatrix(self, mocked_fut_func):
        '''
        Test that the rows and columns are labeled correctly depending on the filenames
        '''
        # assert mock
        self.assertIs(fut.extract_filename, mocked_fut_func)

        # define dummy return values (a different one for each call to this mock)
        expected_filenames = ['file{}'.format(i) for i in range(len(os.listdir(TEST_CODE_FILES)))]
        mocked_fut_func.side_effect = expected_filenames

        # create object and call function to test
        instability_metric = createUUT(TEST_CODE_FILES)
        with patch.object(instability_metric, '_list_of_user_files', os.listdir(TEST_CODE_FILES)):
            instability_metric._create_user_include_matrix()

            # assert correct labeling
            for i, row_label in enumerate(instability_metric._include_matrix.index):
                self.assertEqual(row_label, expected_filenames[i])
            for i, column_label in enumerate(instability_metric._include_matrix.columns):
                self.assertEqual(column_label, expected_filenames[i])


class TestInstabilityMetricFillIncludeMatrix(unittest.TestCase):
    @patch('FileUtility.extract_filename')
    @patch('instability_metric.InstabilityMetric._get_includes_of_file')
    def testCheckMatrixIfNoIncludes(self, mocked_i_func, mocked_fut_func):
        '''
        Test that the member-matrix remains unchanged (only 0s), if no include files are found
        '''
        # assert mocks
        self.assertIs(fut.extract_filename, mocked_fut_func)
        self.assertIs(InstabilityMetric._get_includes_of_file, mocked_i_func)

        # define dummy return values (a different one for each call to this mock)
        expected_filenames = ['file{}'.format(i) for i in range(len(os.listdir(TEST_CODE_FILES)))]
        mocked_fut_func.side_effect = expected_filenames

        empty_user_include_list, empty_std_include_list = [], []
        mocked_i_func.return_value = empty_user_include_list, empty_std_include_list

        mocked_include_matrix = pd.DataFrame(np.zeros((3, 3)), dtype=int)
        expected_include_matrix = pd.DataFrame(np.zeros((3, 3)), dtype=int)

        # create object and call function to test, member-variable is empty
        instability_metric = createUUT()
        with patch.object(instability_metric, '_list_of_user_files', os.listdir(TEST_CODE_FILES)):
            with patch.object(instability_metric, '_include_matrix', mocked_include_matrix):
                instability_metric._fill_include_matrix()

                # assert that mocks are called and the matrix contains 0s only
                mocked_fut_func.assert_called()
                mocked_i_func.assert_called()
                self.assertTrue(instability_metric._include_matrix.equals(expected_include_matrix))

    @patch('FileUtility.extract_filename')
    @patch('instability_metric.InstabilityMetric._get_includes_of_file')
    def testCheckMatrixIfIncludes(self, mocked_i_func, mocked_fut_func):
        '''
        Test that the correct member-matrix is returned, if include files are found
        '''
        # assert mocks
        self.assertIs(fut.extract_filename, mocked_fut_func)
        self.assertIs(InstabilityMetric._get_includes_of_file, mocked_i_func)

        # define dummy return values (a different one for each call to the mocks)
        expected_filenames = ['file{}'.format(i) for i in range(len(os.listdir(TEST_CODE_FILES)))]
        mocked_fut_func.side_effect = expected_filenames
        # each pair defines the respective user or std-lib included files returned by mock
        user_and_std_include_list = [([], ['std_lib']), (['file1'], []), (['file1', 'file2'], ['std_out'])]
        mocked_i_func.side_effect = user_and_std_include_list

        # matrix of shape (m x n), with m being #user-includes and n being (#user-includes + +std-includes)
        expected_std_includes = ['std_lib', 'std_out']
        mocked_include_matrix = pd.DataFrame(np.zeros((3, 5)), index=expected_filenames, columns=expected_filenames +
            expected_std_includes, dtype=int)
        initial_include_matrix = pd.DataFrame(np.zeros((3, 5)), index=expected_filenames, columns=expected_filenames +
            expected_std_includes, dtype=int)

        # create object and call function to test, member-variable is empty
        instability_metric = createUUT()
        with patch.object(instability_metric, '_list_of_user_files', os.listdir(TEST_CODE_FILES)):
            with patch.object(instability_metric, '_include_matrix', mocked_include_matrix):
                instability_metric._fill_include_matrix()

                # assert that mocks are called and the matrix contains 0s only
                mocked_fut_func.assert_called()
                mocked_i_func.assert_called()
                self.assertFalse(instability_metric._include_matrix.equals(initial_include_matrix))

                # iterate through matrix and check for 1s and 0s
                for i, row_label in enumerate(instability_metric._include_matrix.index):
                    for column_label in instability_metric._include_matrix.columns:
                        # matrix[i][j] should contain 1 iff j is contained in i-th tuple of 'user_and_std_include_list' above
                        expected_entry = 0
                        if column_label in user_and_std_include_list[i][0] or column_label in user_and_std_include_list[i][1]:
                            expected_entry = 1

                        self.assertEqual(instability_metric._include_matrix.loc[row_label, column_label], expected_entry)


class TestInstabilityMetricAddStlIncludes(unittest.TestCase):
    @patch('FileUtility.extract_filename')
    @patch('instability_metric.InstabilityMetric._get_includes_of_file')
    def testEmtpyStlIncludes(self, mocked_i_func, mocked_fut_func):
        '''
        Test that no column is added to existing matrix if no STL includes are found
        '''
        # assert mocks
        self.assertIs(fut.extract_filename, mocked_fut_func)
        self.assertIs(InstabilityMetric._get_includes_of_file, mocked_i_func)

        # define dummy return values (a different one for each call to the mocks)
        expected_filenames = ['file{}'.format(i) for i in range(len(os.listdir(TEST_CODE_FILES)))]
        mocked_fut_func.side_effect = expected_filenames
        # each pair defines the respective user or std-lib included files returned by mock
        empty_user_and_std_include_list = [([], []) for i in range(len(expected_filenames))]
        mocked_i_func.side_effect = empty_user_and_std_include_list

        mocked_include_matrix = pd.DataFrame(np.zeros((3, 3)), dtype=int)
        expected_include_matrix = pd.DataFrame(np.zeros((3, 3)), dtype=int)

        # create object and call function to test, member-variable is empty
        instability_metric = createUUT()
        with patch.object(instability_metric, '_list_of_user_files', os.listdir(TEST_CODE_FILES)):
            with patch.object(instability_metric, '_include_matrix', mocked_include_matrix):
                instability_metric._add_stl_includes()

                # assert that mocks are called and the matrix was not extended
                mocked_fut_func.assert_called()
                mocked_i_func.assert_called()
                self.assertTrue(instability_metric._include_matrix.equals(expected_include_matrix))
                self.assertEqual(instability_metric._include_matrix.shape, expected_include_matrix.shape)

    @patch('FileUtility.extract_filename')
    @patch('instability_metric.InstabilityMetric._get_includes_of_file')
    def testNonEmtpyStlIncludes(self, mocked_i_func, mocked_fut_func):
        '''
        Test that columns are added to existing matrix if STL includes are found
        '''
        # assert mocks
        self.assertIs(fut.extract_filename, mocked_fut_func)
        self.assertIs(InstabilityMetric._get_includes_of_file, mocked_i_func)

        # define dummy return values (a different one for each call to the mocks)
        expected_filenames = ['file{}'.format(i) for i in range(len(os.listdir(TEST_CODE_FILES)))]
        mocked_fut_func.side_effect = expected_filenames
        # each pair defines the respective user or std-lib included files returned by mock
        user_and_std_include_list = [([], ['std_lib']), (['file1'], []), (['file1', 'file2'], ['std_out'])]
        mocked_i_func.side_effect = user_and_std_include_list

        mocked_include_matrix = pd.DataFrame(np.zeros((3, 3)), dtype=int)
        expected_include_matrix_shape = (3, 5)

        # create object and call function to test
        instability_metric = createUUT()
        with patch.object(instability_metric, '_list_of_user_files', os.listdir(TEST_CODE_FILES)):
            with patch.object(instability_metric, '_include_matrix', mocked_include_matrix):
                instability_metric._add_stl_includes()

                # assert that mocks are called and the matrix was extended by two columns
                mocked_fut_func.assert_called()
                mocked_i_func.assert_called()
                self.assertEqual(instability_metric._include_matrix.shape, expected_include_matrix_shape)

    @patch('FileUtility.extract_filename')
    @patch('instability_metric.InstabilityMetric._get_includes_of_file')
    def testNoDuplicatedStlIncludes(self, mocked_i_func, mocked_fut_func):
        '''
        Test that duplicated stl-includes are added as a single column
        '''
        # assert mocks
        self.assertIs(fut.extract_filename, mocked_fut_func)
        self.assertIs(InstabilityMetric._get_includes_of_file, mocked_i_func)

        # define dummy return values (a different one for each call to the mocks)
        expected_filenames = ['file{}'.format(i) for i in range(len(os.listdir(TEST_CODE_FILES)))]
        mocked_fut_func.side_effect = expected_filenames
        # each pair defines the respective user or std-lib included files returned by mock
        user_and_std_include_list = [([], ['std_lib']), (['file1'], []), (['file1', 'file2'], ['std_lib'])]
        mocked_i_func.side_effect = user_and_std_include_list

        mocked_include_matrix = pd.DataFrame(np.zeros((3, 3)), dtype=int)
        expected_include_matrix_shape = (3, 4)

        # create object and call function to test
        instability_metric = createUUT()
        with patch.object(instability_metric, '_list_of_user_files', os.listdir(TEST_CODE_FILES)):
            with patch.object(instability_metric, '_include_matrix', mocked_include_matrix):
                instability_metric._add_stl_includes()

                # assert that mocks are called and the matrix was extended by 1 column only
                mocked_fut_func.assert_called()
                mocked_i_func.assert_called()
                self.assertEqual(instability_metric._include_matrix.shape, expected_include_matrix_shape)


class TestInstabilityMetricGetAllFanIn(unittest.TestCase):
    def testCorrectReturnValue(self):
        '''
        Test that the correct value is returned
        '''
        mocked_include_matrix = pd.DataFrame([[0,1,0], [1,1,1], [0,0,0]], dtype=int)

        # create object and call function to test
        instability_metric = createUUT()
        with patch.object(instability_metric, '_include_matrix', mocked_include_matrix):
            returned_sum_matrix = instability_metric._get_all_fan_in()

            # assert correct return value
            self.assertTrue(returned_sum_matrix.equals(np.sum(instability_metric._include_matrix, axis=1)))


class TestInstabilityMetricGetAllFanOut(unittest.TestCase):
    def testCorrectReturnValue(self):
        '''
        Test that the correct value is returned
        '''
        mocked_include_matrix = pd.DataFrame([[0,1,0], [1,1,1], [0,0,0]], dtype=int)

        # create object and call function to test
        instability_metric = createUUT()
        with patch.object(instability_metric, '_include_matrix', mocked_include_matrix):
            returned_sum_matrix = instability_metric._get_all_fan_out()

            # assert correct return value
            self.assertTrue(returned_sum_matrix.equals(np.sum(instability_metric._include_matrix, axis=0)))
            
            
class TestInstabilityMetricCalculateInstabilityForEachFile(unittest.TestCase):
    @patch('instability_metric.InstabilityMetric._get_all_fan_out')
    @patch('instability_metric.InstabilityMetric._get_all_fan_in')
    def testCorrectCalculation(self, mocked_i_func_in, mocked_i_func_out):
        '''
        Test that a the instability metric is computed correctly
        '''
        # assert mocks
        self.assertIs(InstabilityMetric._get_all_fan_in, mocked_i_func_in)
        self.assertIs(InstabilityMetric._get_all_fan_out, mocked_i_func_out)
        
        # create matrix mock
        matrix_mock = pd.DataFrame(index=['file1', 'file2', 'file3'], columns=['file1', 'file2', 'file3', 'std_lib', 'std_out'], dtype=int)
        matrix_mock.loc['file1', :] = [0, 1, 0, 1, 0]
        matrix_mock.loc['file2', :] = [0, 0, 0, 0, 1]
        matrix_mock.loc['file3', :] = [1, 0, 0, 0, 0]
        
        # define return values (a different one for each call to the mocks)
        expected_sum_fan_in = np.sum(matrix_mock, axis=1)
        expected_sum_fan_out = np.sum(matrix_mock, axis=0)
        mocked_i_func_in.return_value = expected_sum_fan_in
        mocked_i_func_out.return_value = expected_sum_fan_out
        
        # create object and call function to test
        instability_metric = createUUT()
        returned_matrix = instability_metric._calculate_instability_for_each_file()

        # assert mock calls
        mocked_i_func_in.assert_called_once()
        mocked_i_func_out.assert_called_once()
        
        # assert correct matrix shape (rows, 1)
        self.assertEqual(returned_matrix.shape, (len(matrix_mock.index),))
        
        # assert correct computation of instability metric
        for i in range(len(returned_matrix.index)):
            self.assertEqual(returned_matrix[i], (expected_sum_fan_out[i] / (expected_sum_fan_in[i] + expected_sum_fan_out[i])))
            
      
class TestInstabilityMetricComputeInstability(unittest.TestCase):
    @patch('FileUtility.get_all_code_files')
    @patch('instability_metric.InstabilityMetric._create_user_include_matrix')
    @patch('instability_metric.InstabilityMetric._add_stl_includes')
    @patch('instability_metric.InstabilityMetric._fill_include_matrix')
    @patch('instability_metric.InstabilityMetric._calculate_instability_for_each_file')
    def testCorrectFunctionCallsWithEmptyFilePath(self, mocked_i_calc_func, mocked_i_fill_func, mocked_i_add_func, 
    mocked_i_create_func, mocked_fut_get_func):
        '''
        Test that the correct functions are invoked when an empty filepath was provided
        '''
        # assert mocks
        self.assertIs(InstabilityMetric._calculate_instability_for_each_file, mocked_i_calc_func)
        self.assertIs(InstabilityMetric._fill_include_matrix, mocked_i_fill_func)
        self.assertIs(InstabilityMetric._add_stl_includes, mocked_i_add_func)
        self.assertIs(InstabilityMetric._create_user_include_matrix, mocked_i_create_func)
        self.assertIs(fut.get_all_code_files, mocked_fut_get_func)

        # create object and call function to test
        instability_metric = createUUT()
        instability_metric.compute_instability()

        # assert function calls
        mocked_fut_get_func.assert_called_once()
        mocked_i_create_func.assert_called_once()
        mocked_i_add_func.assert_called_once()
        mocked_i_fill_func.assert_called_once()
        mocked_i_calc_func.assert_called_once()
        
    @patch('FileUtility.get_all_code_files')
    @patch('instability_metric.InstabilityMetric._create_user_include_matrix')
    @patch('instability_metric.InstabilityMetric._add_stl_includes')
    @patch('instability_metric.InstabilityMetric._fill_include_matrix')
    @patch('instability_metric.InstabilityMetric._calculate_instability_for_each_file')
    def testCorrectFunctionCallsWithNonEmptyFilePath(self, mocked_i_calc_func, mocked_i_fill_func, mocked_i_add_func, 
    mocked_i_create_func, mocked_fut_get_func):
        '''
        Test that the correct functions are invoked when a correct filepath was provided
        '''
        # assert mocks
        self.assertIs(InstabilityMetric._calculate_instability_for_each_file, mocked_i_calc_func)
        self.assertIs(InstabilityMetric._fill_include_matrix, mocked_i_fill_func)
        self.assertIs(InstabilityMetric._add_stl_includes, mocked_i_add_func)
        self.assertIs(InstabilityMetric._create_user_include_matrix, mocked_i_create_func)
        self.assertIs(fut.get_all_code_files, mocked_fut_get_func)

        # create object and call function to test
        instability_metric = createUUT(TEST_CODE_FILES)
        instability_metric.compute_instability()

        # assert function calls
        mocked_fut_get_func.assert_called_once()
        mocked_i_create_func.assert_called_once()
        mocked_i_add_func.assert_called_once()
        mocked_i_fill_func.assert_called_once()
        mocked_i_calc_func.assert_called_once()


# create TestSuite with above TestCases
suite = unittest.TestSuite()
suite.addTests(unittest.makeSuite(TestInstabilityMetricGetIncludesOfFile))
suite.addTests(unittest.makeSuite(TestInstabilityMetricCreateUserIncludeMatrix))
suite.addTests(unittest.makeSuite(TestInstabilityMetricFillIncludeMatrix))
suite.addTests(unittest.makeSuite(TestInstabilityMetricAddStlIncludes))
suite.addTests(unittest.makeSuite(TestInstabilityMetricGetAllFanIn))
suite.addTests(unittest.makeSuite(TestInstabilityMetricGetAllFanOut))
suite.addTests(unittest.makeSuite(TestInstabilityMetricCalculateInstabilityForEachFile))
suite.addTests(unittest.makeSuite(TestInstabilityMetricComputeInstability))

# run TestSuite
unittest.TextTestRunner(verbosity=2).run(suite)

