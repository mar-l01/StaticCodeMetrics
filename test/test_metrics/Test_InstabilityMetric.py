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
HEADER_FILE_1 = TEST_CODE_FILES + 'lib1.hpp'
HEADER_FILE_2 = TEST_CODE_FILES + 'lib2.hpp'
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
            
           
# create TestSuite with above TestCases
suite = unittest.TestSuite()
suite.addTests(unittest.makeSuite(TestInstabilityMetricGetIncludesOfFile))

# run TestSuite
unittest.TextTestRunner(verbosity=2).run(suite)

