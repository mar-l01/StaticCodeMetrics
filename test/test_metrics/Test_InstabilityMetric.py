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
        

# create TestSuite with above TestCases
suite = unittest.TestSuite()
suite.addTests(unittest.makeSuite(TestInstabilityMetricGetIncludesOfFile))
suite.addTests(unittest.makeSuite(TestInstabilityMetricCreateUserIncludeMatrix))

# run TestSuite
unittest.TextTestRunner(verbosity=2).run(suite)

