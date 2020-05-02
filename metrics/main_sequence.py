import matplotlib.pyplot as plt
import numpy as np
import sys
import warnings

# make utility scripts visible
sys.path.append('utils/')
import DataSeriesUtility as dsu
import FileUtility as fut


class MainSequence:
    def __init__(self, dir_path):
        self._dir_path = dir_path
        self._annotation_points = []
        self._last_hov_anno_index = -1
        self._instability_metric = None
        self._abstractness_metric = None

    def _annotate_point(self, event, sc):  # noqa: C901
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
                    if annotation.get_visible():
                        annotation.set_visible(False)
                        visibility_changed = True

            # only one annotation available
            elif ind_array.size == 1:
                if not self._annotation_points[ind_array[0]].get_visible():
                    self._annotation_points[ind_array[0]].set_visible(True)
                    visibility_changed = True

            # more than one annotation available (display only one)
            else:
                # again hovered over the same summary of points
                if self._last_hov_anno_index in ind_array:
                    # do not change annotation if mouse still is on point
                    if self._annotation_points[self._last_hov_anno_index].get_visible():
                        return

                    # get array index and increment it
                    arr_ind, = np.where(ind_array == self._last_hov_anno_index)
                    next_arr_ind = arr_ind[0] + 1

                    # start from beginning if end of array indices is reached
                    if next_arr_ind == ind_array.size:
                        next_arr_ind = 0

                    # map array index to annotation index
                    anno_ind = ind_array[next_arr_ind]

                    # set respective annotation visible
                    self._annotation_points[anno_ind].set_visible(True)
                    visibility_changed = True
                    self._last_hov_anno_index = anno_ind

                # hovered over another summary of points
                else:
                    self._annotation_points[ind_array[0]].set_visible(True)
                    visibility_changed = True
                    self._last_hov_anno_index = ind_array[0]

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
        self._annotation_points = [ax.annotate(n, (x, y), visible=False) for n, x, y in
                                   zip(self._instability_metric.index, self._instability_metric, self._abstractness_metric)]

        # x = instability, y = abstractness
        sc = ax.scatter(self._instability_metric, self._abstractness_metric)

        # use a motion-event to display annotations
        self._define_motion_annotation_callback(sc)

        plt.show()

    def save_metrics(self, dir_path=''):
        ''' save both metrics to directory. If provided use user-defined directory '''
        # if not already computed get metrics
        if self._instability_metric is None or self._abstractness_metric is None:
            self._instability_metric, self._abstractness_metric = dsu.get_instability_and_abstractness_metric(self._dir_path)

        # save them
        fut.save_metric_to_file(self._instability_metric, dir_path)
        fut.save_metric_to_file(self._abstractness_metric, dir_path)
