from instability_metric import InstabilityMetric
from abstractness_metric import AbstractnessMetric

import matplotlib.pyplot as plt
import pandas as pd


# global instance of currently visible annotation text
annotated_point = None


def calculate_main_sequence(dir_path):
    ''' helper-function called when plotting the Main Sequence.
    If one array is of lower size than the other, it has to be extended with
    the default values to be able to plot it '''
    instability_metric = InstabilityMetric(dir_path)
    instability_metric = instability_metric.compute_instability()
    
    abstractness_metric = AbstractnessMetric(dir_path)
    abstractness_metric = abstractness_metric.compute_abstractness()

    # for each instability-value an abstractness-value needs to exist
    if len(instability_metric) > len(abstractness_metric):
        abstractness_metric = pad_data_series_with_default_values(instability_metric, abstractness_metric, 0)
    # for each abstractness-value an instability-value needs to exist
    elif len(abstractness_metric) > len(instability_metric):
        instability_metric = pad_data_series_with_default_values(abstractness_metric, instability_metric, 0)

    # order elements of array the same
    abstractness_metric = reorder_data_series_elements(instability_metric, abstractness_metric)

    return instability_metric, abstractness_metric


def pad_data_series_with_default_values(data_series, data_series_to_pad, default_value):
    ''' pad data_series_to_pad with default values to be the same size as data_series
    and contain the same index-names, too. Return the padded data-series '''
    padded_data_series = data_series_to_pad   
    for index_name in data_series.index:
        if index_name not in data_series_to_pad:
            padded_data_series[index_name] = default_value

    return padded_data_series


def reorder_data_series_elements(data_series, data_series_to_reorder):
    ''' order elements in data_series_to_reorder the same way as they are in data_series '''
    ordered_data_series = pd.Series(dtype=int)
    for index_name in data_series.index:
        ordered_data_series[index_name] = data_series_to_reorder[index_name]

    return ordered_data_series
    

def plot_metrics(dir_path):
    ''' show a diagram picturing the Main Sequence, where
    - y-axis denotes the Abstractness
    - x-axis denotes the Instability '''
    instability, abstractness = calculate_main_sequence(dir_path)
    
    ax = plt.gca()

    # x/y range from 0 to 1
    ax.set_xlim((0, 1))
    ax.set_ylim((0, 1))

    # Main Sequence
    ax.plot([0,1], [1,0], marker='x', color='red')
    # zone of pain
    ax.add_artist(plt.Circle((0, 0), .5, alpha=.3, color='r', label="test"))
    ax.annotate("Zone of Pain", xy=(.1, .2), fontsize=10)

    # zone of uselessness
    ax.add_artist(plt.Circle((1, 1), .5, alpha=.3, color='r'))
    ax.annotate("Zone of Uselessness", xy=(.65, .8), fontsize=10)

    # x = instability, y = abstractness
    sc = ax.scatter(instability, abstractness)
    
    ax.set_xlabel('[I]nstability', fontsize=18)
    ax.set_ylabel('[A]bstractness', fontsize=18)

    # annotate points if one hovers over it with the mouse
    names_map = [(n, (x, y)) for n, x, y in zip(instability.index, instability, abstractness)]
    
    global annotated_point
    annotated_point = ax.annotate(*names_map[0])
    annotated_point.set_visible(False)
    
    # callback executed at each mouse motion event
    annotation_callback = lambda event: annotate_point(event, ax, sc, names_map)
    
    fig = plt.gcf()
    fig.canvas.set_window_title('Main Sequence')
    fig.canvas.mpl_connect("motion_notify_event", lambda event: annotation_callback(event))

    plt.show()


def annotate_point(event, ax, sc, names_map):
    ''' displays a text, if a user hovers over a point with the mouse '''
    fig = plt.gcf()
    global annotated_point

    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            annotated_point = ax.annotate(*names_map[ind['ind'][0]])
            annotated_point.set_visible(True)
            fig.canvas.draw_idle()
        else:
            annotated_point.set_visible(False)
            fig.canvas.draw_idle()


if __name__ == '__main__':
    directory_path = '../../cppmodbus/src/cppmodbus/'
    plot_metrics(directory_path)
