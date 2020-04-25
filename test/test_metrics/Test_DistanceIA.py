import numpy as np
import os
import pandas as pd
import unittest
from unittest.mock import patch
import sys

# make utility scripts visible
sys.path.append('utils/')
import DataSeriesUtility as dsu

sys.path.append('metrics/')
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

        distance_ia = createUUT()

        with patch.object(distance_ia, '_instability_metric', mocked_i_metric):
            with patch.object(distance_ia, '_abstractness_metric', mocked_a_metric):
                distance_ia._calculate_distance()

                self.assertTrue(distance_ia._distance.equals(expected_calc_distance))


# create TestSuite with above TestCases
suite = unittest.TestSuite()
suite.addTests(unittest.makeSuite(TestDistanceIACalculateDistance))

# run TestSuite
unittest.TextTestRunner(verbosity=2).run(suite)

