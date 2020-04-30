from instability_metric import InstabilityMetric
from abstractness_metric import AbstractnessMetric

import matplotlib.pyplot as plt
import numpy as np
import sys
import warnings

# make utility scripts visible
sys.path.append('utils/')
import DataSeriesUtility as dsu


class MainSequence:
    def __init__(self, dir_path):
        self._dir_path = dir_path
        self._annotated_point = None
        self._annotation_points = []

    def _annotate_point(self, event, sc):
        ''' displays a text, if a user hovers over a point with the mouse '''
        fig = plt.gcf()
        visibility_changed = False
        
        if event.inaxes == plt.gca():
            anno_visible, ind = sc.contains(event)
            ind_array = ind['ind']
            
            # check if not hovering over a point (empty index list)
            if ind_array.size == 0:
                for annotation in self._annotation_points:
                    # make sure every annotation is invisible
                    if annotation.get_visible() == True:
                        annotation.set_visible(False)
                        visibility_changed = True
            else:
                # set all annotations visible which the mouse hovers over
                for i, annotation in enumerate(self._annotation_points):
                    if np.any(ind_array == i) and annotation.get_visible() == False:
                        annotation.set_visible(True)
                        visibility_changed = True
        
        if visibility_changed:
            fig.canvas.draw_idle()

    def _layout_ax(self):
        ''' creates and returns the basic layout of the diagram displayed '''
        ax = plt.gca()

        # x/y range from 0 to 1
        ax.set_xlim((0, 1))
        ax.set_ylim((0, 1))

        # Main Sequence
        ax.plot([0, 1], [1, 0], marker='x', color='red')

        # zone of pain
        ax.add_artist(plt.Circle((0, 0), .5, alpha=.3, color='r'))
        ax.annotate("Zone of Pain", xy=(.1, .2), fontsize=10)

        # zone of uselessness
        ax.add_artist(plt.Circle((1, 1), .5, alpha=.3, color='r'))
        ax.annotate("Zone of Uselessness", xy=(.65, .8), fontsize=10)

        # label x and y
        ax.set_xlabel('[I]nstability', fontsize=18)
        ax.set_ylabel('[A]bstractness', fontsize=18)

        return ax

    def _define_motion_annotation_callback(self, sc):
        ''' fill displayed diagram with a mouse-event to show annotations within it '''
        fig = plt.gcf()
        fig.canvas.set_window_title('Main Sequence')

        # check for empty name map
        if self._annotation_points == []:
            warnings.warn('"self._names_map" is empty...returning directly, no motion_notifiy_event connected')
            return

        # callback executed at each mouse motion event
        fig.canvas.mpl_connect("motion_notify_event", lambda event: self._annotate_point(event, sc))

    def plot_metrics(self):
        ''' show a diagram picturing the Main Sequence, where
        - y-axis denotes the Abstractness
        - x-axis denotes the Instability '''
        self._instability_metric, self._abstractness_metric = dsu.get_instability_and_abstractness_metric(self._dir_path)

        # create basic layout format
        ax = self._layout_ax()
        
        # create a list which contains all annotations
        self._annotation_points = [ax.annotate(n, (x,y), visible=False) for n, x, y in \
            zip(self._instability_metric.index, self._instability_metric, self._abstractness_metric)]

        # x = instability, y = abstractness
        sc = ax.scatter(self._instability_metric, self._abstractness_metric)

        # use a motion-event to display annotations
        self._define_motion_annotation_callback(sc)

        plt.show()
