import numpy as np
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
TEST_CODE_FILES = 'test/files/'
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
        returned_nb_interfaces, returned_nb_classes = abstractness_metric._get_number_of_interfaces_and_classes_of_file(ABSTRACT_CLASS_FILE)

        # assert correct result
        self.assertEqual(returned_nb_interfaces, 1)
        self.assertEqual(returned_nb_classes, 1)  
        
    def testNonAbstractClassFile(self):
        '''
        Test that no abstract class is found
        '''
        # create object and call function to test
        abstractness_metric = createUUT()
        returned_nb_interfaces, returned_nb_classes = abstractness_metric._get_number_of_interfaces_and_classes_of_file(NON_ABSTRACT_CLASS_FILE)

        # assert correct result
        self.assertEqual(returned_nb_interfaces, 0)
        self.assertEqual(returned_nb_classes, 1)


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
        

# create TestSuite with above TestCases
suite = unittest.TestSuite()
suite.addTests(unittest.makeSuite(TestAbstractnessMetricGetNumberOfInterfacesAndClassesOfFile))
suite.addTests(unittest.makeSuite(TestAbstractnessMetricComputeAbstractness))

# run TestSuite
unittest.TextTestRunner(verbosity=2).run(suite)

