import unittest
import sys

sys.path.append('test/test_utils/')
import Test_FileUtility as t_fu
import Test_DataSeriesUtility as t_dsu

sys.path.append('test/test_metrics')
import Test_AbstractnessMetric as t_am
import Test_InstabilityMetric as t_im
import Test_DistanceIA as t_dia
import Test_MainSequence as t_ms

# create TestSuite with all testcases
suite = unittest.TestSuite()

# FileUtility
suite.addTests(unittest.makeSuite(t_fu.TestFileUtilityGetAllCodeFiles))
suite.addTests(unittest.makeSuite(t_fu.TestFileUtilityExtractFileName))
suite.addTests(unittest.makeSuite(t_fu.TestFileUtilitySaveMetricToFile))

# DataSeriesUtility
suite.addTests(unittest.makeSuite(t_dsu.TestDataSeriesUtilityGetInstabilityAndAbstractnessMetric))
suite.addTests(unittest.makeSuite(t_dsu.TestDataSeriesUtilityPadDataSeriesWithDefaultValues))
suite.addTests(unittest.makeSuite(t_dsu.TestReorderDataSeriesElements))

# AbstractnessMetric
suite.addTests(unittest.makeSuite(t_am.TestAbstractnessMetricGetNumberOfInterfacesAndClassesOfFile))
suite.addTests(unittest.makeSuite(t_am.TestAbstractnessMetricCalculateAbstractnessForEachFile))
suite.addTests(unittest.makeSuite(t_am.TestAbstractnessMetricSearchFilesForInterfaces))
suite.addTests(unittest.makeSuite(t_am.TestAbstractnessMetricComputeAbstractness))

# InstabilityMetric
suite.addTests(unittest.makeSuite(t_im.TestInstabilityMetricGetIncludesOfFile))
suite.addTests(unittest.makeSuite(t_im.TestInstabilityMetricCreateUserIncludeMatrix))
suite.addTests(unittest.makeSuite(t_im.TestInstabilityMetricFillIncludeMatrix))
suite.addTests(unittest.makeSuite(t_im.TestInstabilityMetricAddStlIncludes))
suite.addTests(unittest.makeSuite(t_im.TestInstabilityMetricGetAllFanIn))
suite.addTests(unittest.makeSuite(t_im.TestInstabilityMetricGetAllFanOut))
suite.addTests(unittest.makeSuite(t_im.TestInstabilityMetricCalculateInstabilityForEachFile))
suite.addTests(unittest.makeSuite(t_im.TestInstabilityMetricComputeInstability))

# DistanceIA
suite.addTests(unittest.makeSuite(t_dia.TestDistanceIACalculateDistance))
suite.addTests(unittest.makeSuite(t_dia.TestDistanceIAPlotDistance))

# MainSequence
suite.addTests(unittest.makeSuite(t_ms.TestMainSequenceAnnotatePoint))
suite.addTests(unittest.makeSuite(t_ms.TestMainSequenceLayoutAx))
suite.addTests(unittest.makeSuite(t_ms.TestMainSequenceDefineMotionAnnotationCallback))
suite.addTests(unittest.makeSuite(t_ms.TestMainSequencePlotMetrics))

# run TestSuite
result = unittest.TextTestRunner(verbosity=2).run(suite)

# exit with with success if testcases ran successfully, otw. with error
if result.wasSuccessful():
    sys.exit(0)
else:
    sys.exit(1)
