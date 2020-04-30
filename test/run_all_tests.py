import unittest
import sys

sys.path.append('test/test_utils/')
from Test_FileUtility import *
from Test_DataSeriesUtility import *

sys.path.append('test/test_metrics')
from Test_AbstractnessMetric import *
from Test_InstabilityMetric import *
from Test_DistanceIA import *
from Test_MainSequence import *

# create TestSuite with all testcases
suite = unittest.TestSuite()

# FileUtility
suite.addTests(unittest.makeSuite(TestFileUtilityGetAllCodeFiles))
suite.addTests(unittest.makeSuite(TestFileUtilityExtractFileName))

# DataSeriesUtility
suite.addTests(unittest.makeSuite(TestDataSeriesUtilityGetInstabilityAndAbstractnessMetric))
suite.addTests(unittest.makeSuite(TestDataSeriesUtilityPadDataSeriesWithDefaultValues))
suite.addTests(unittest.makeSuite(TestReorderDataSeriesElements))

# AbstractnessMetric
suite.addTests(unittest.makeSuite(TestAbstractnessMetricGetNumberOfInterfacesAndClassesOfFile))
suite.addTests(unittest.makeSuite(TestAbstractnessMetricCalculateAbstractnessForEachFile))
suite.addTests(unittest.makeSuite(TestAbstractnessMetricSearchFilesForInterfaces))
suite.addTests(unittest.makeSuite(TestAbstractnessMetricComputeAbstractness))

# InstabilityMetric
suite.addTests(unittest.makeSuite(TestInstabilityMetricGetIncludesOfFile))
suite.addTests(unittest.makeSuite(TestInstabilityMetricCreateUserIncludeMatrix))
suite.addTests(unittest.makeSuite(TestInstabilityMetricFillIncludeMatrix))
suite.addTests(unittest.makeSuite(TestInstabilityMetricAddStlIncludes))
suite.addTests(unittest.makeSuite(TestInstabilityMetricGetAllFanIn))
suite.addTests(unittest.makeSuite(TestInstabilityMetricGetAllFanOut))
suite.addTests(unittest.makeSuite(TestInstabilityMetricCalculateInstabilityForEachFile))
suite.addTests(unittest.makeSuite(TestInstabilityMetricComputeInstability))

# DistanceIA
suite.addTests(unittest.makeSuite(TestDistanceIACalculateDistance))
suite.addTests(unittest.makeSuite(TestDistanceIAPlotDistance))

# MainSequence
suite.addTests(unittest.makeSuite(TestMainSequenceAnnotatePoint))
suite.addTests(unittest.makeSuite(TestMainSequenceLayoutAx))
suite.addTests(unittest.makeSuite(TestMainSequenceDefineMotionAnnotationCallback))
suite.addTests(unittest.makeSuite(TestMainSequencePlotMetrics))

# run TestSuite
result = unittest.TextTestRunner(verbosity=2).run(suite)

# exit with with success if testcases ran successfully, otw. with error
if result.wasSuccessful():
    sys.exit(0)
else:
    sys.exit(1)
