from instability_metric import InstabilityMetric
from abstractness_metric import AbstractnessMetric

import matplotlib.pyplot as plt
import pandas as pd
import sys

# make utility scripts visible
sys.path.append('../utils/')
import DataSeriesUtility as dsu


class MainSequence:
    def __init__(self, dir_path):
        self._dir_path = dir_path


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
        self._instability_metric, self._abstractness_metric = dsu.get_instability_and_abstractness_metric(self._dir_path)
        # create a map which assigns file/component names to their coordinates
        self._names_map = [(n, (x, y)) for n, x, y in zip(self._instability_metric.index, self._instability_metric, self._abstractness_metric)]


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
