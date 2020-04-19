from instability_metric import InstabilityMetric
from abstractness_metric import AbstractnessMetric

import matplotlib.pyplot as plt
import pandas as pd


# default value used to pad data-sequences to required size
DEFAULT_PADDING_VALUE = 0


class MainSequence:
    def __init__(self, dir_path):
        self._dir_path = dir_path


    def _set_instability_and_abstractness_metric(self):
        ''' helper-function called when plotting the Main Sequence.
        If one array is of lower size than the other, it has to be extended with
        the default values to be able to plot it. To be further able to show names with
        plotted points a names-map is created which assigns each filename its coordinates '''
        instabilityMetric = InstabilityMetric(self._dir_path)
        instability_metric = instabilityMetric.compute_instability()

        abstractnessMetric = AbstractnessMetric(self._dir_path)
        abstractness_metric = abstractnessMetric.compute_abstractness()

        # for each instability-value an abstractness-value needs to exist
        if len(instability_metric) > len(abstractness_metric):
            abstractness_metric = self._pad_data_series_with_default_values(instability_metric, abstractness_metric)
        # for each abstractness-value an instability-value needs to exist
        elif len(abstractness_metric) > len(instability_metric):
            instability_metric = self._pad_data_series_with_default_values(abstractness_metric, instability_metric)

        # order elements of array the same
        abstractness_metric = self._reorder_data_series_elements(instability_metric, abstractness_metric)

        # set both metrics as members
        self._instability_metric = instability_metric
        self._abstractness_metric = abstractness_metric

        # create a map which assigns file/component names to their coordinates
        self._names_map = [(n, (x, y)) for n, x, y in zip(self._instability_metric.index, self._instability_metric, self._abstractness_metric)]


    def _pad_data_series_with_default_values(self, data_series, data_series_to_pad):
        ''' pad data_series_to_pad with default values to be the same size as data_series
        and contain the same index-names, too. Return the padded data-series '''
        padded_data_series = data_series_to_pad
        for index_name in data_series.index:
            if index_name not in data_series_to_pad:
                padded_data_series[index_name] = DEFAULT_PADDING_VALUE

        return padded_data_series


    def _reorder_data_series_elements(self, data_series, data_series_to_reorder):
        ''' order elements in data_series_to_reorder the same way as they are in data_series '''
        ordered_data_series = pd.Series(dtype=int)
        for index_name in data_series.index:
            ordered_data_series[index_name] = data_series_to_reorder[index_name]

        return ordered_data_series


    def _annotate_point(self, event, ax, sc):
        ''' displays a text, if a user hovers over a point with the mouse '''
        fig = plt.gcf()

        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                self._annotated_point = ax.annotate(*self._names_map[ind['ind'][0]])
                self._annotated_point.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if self._annotated_point.get_visible():
                    self._annotated_point.set_visible(False)
                    fig.canvas.draw_idle()


    def plot_metrics(self):
        ''' show a diagram picturing the Main Sequence, where
        - y-axis denotes the Abstractness
        - x-axis denotes the Instability '''
        self._set_instability_and_abstractness_metric()

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
        sc = ax.scatter(self._instability_metric, self._abstractness_metric)

        ax.set_xlabel('[I]nstability', fontsize=18)
        ax.set_ylabel('[A]bstractness', fontsize=18)

        # annotate points if one hovers over it with the mouse
        self._annotated_point = ax.annotate(*self._names_map[0])
        self._annotated_point.set_visible(False)

        # callback executed at each mouse motion event
        annotation_callback = lambda event: self._annotate_point(event, ax, sc)

        fig = plt.gcf()
        fig.canvas.set_window_title('Main Sequence')
        fig.canvas.mpl_connect("motion_notify_event", lambda event: annotation_callback(event))

        plt.show()


if __name__ == '__main__':
    directory_path = '../../cppmodbus/src/cppmodbus/'
    mainSequence = MainSequence(directory_path)
    mainSequence.plot_metrics()
