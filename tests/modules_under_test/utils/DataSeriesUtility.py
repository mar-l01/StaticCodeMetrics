import pandas as pd

import sys
sys.path.append('tests/modules_under_test/metrics/')
from instability_metric import InstabilityMetric
from abstractness_metric import AbstractnessMetric

# default value used to pad data-sequences to required size
DEFAULT_PADDING_VALUE = 0


def get_instability_and_abstractness_metric(dir_path):
    ''' return instability and abstractness metric. If one array is of lower size than the other,
    it has to be extended with the default values to be able to plot it '''
    instabilityMetric = InstabilityMetric(dir_path)
    instability_metric = instabilityMetric.compute_instability()

    abstractnessMetric = AbstractnessMetric(dir_path)
    abstractness_metric = abstractnessMetric.compute_abstractness()

    # for each instability-value an abstractness-value needs to exist
    if len(instability_metric) > len(abstractness_metric):
        abstractness_metric = pad_data_series_with_default_values(instability_metric, abstractness_metric)
    # for each abstractness-value an instability-value needs to exist
    elif len(abstractness_metric) > len(instability_metric):
        instability_metric = pad_data_series_with_default_values(abstractness_metric, instability_metric)

    # order elements of array the same
    abstractness_metric = reorder_data_series_elements(instability_metric, abstractness_metric)

    # return both metrics
    return instability_metric, abstractness_metric


def pad_data_series_with_default_values(data_series, data_series_to_pad):
    ''' pad data_series_to_pad with default values to be the same size as data_series
    and contain the same index-names, too. Return the padded data-series '''
    if not isinstance(data_series, type(pd.Series(dtype=float))) or \
       not isinstance(data_series_to_pad, type(pd.Series(dtype=float))):
        return pd.Series(dtype=float)

    padded_data_series = data_series_to_pad
    for index_name in data_series.index:
        if index_name not in data_series_to_pad:
            padded_data_series[index_name] = DEFAULT_PADDING_VALUE

    return padded_data_series


def reorder_data_series_elements(data_series, data_series_to_reorder):
    ''' order elements in data_series_to_reorder the same way as they are in data_series '''
    if not isinstance(data_series, type(pd.Series(dtype=float))) or \
       not isinstance(data_series_to_reorder, type(pd.Series(dtype=float))):
        return pd.Series(dtype=float)

    ordered_data_series = pd.Series(name=data_series_to_reorder.name, dtype=float)
    for index_name in data_series.index:
        ordered_data_series[index_name] = data_series_to_reorder[index_name]

    return ordered_data_series
