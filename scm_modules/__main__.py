import argparse
import sys

# make main-sequence script visible
sys.path.append('scm_modules/metrics/')
from main_sequence import MainSequence
from distance_ia import DistanceIA

sys.path.append('scm_modules/utils/')
import ProgrammingLanguageConfig as plc


def main():
    # init parser
    parser = argparse.ArgumentParser(description='Perform static code checks on a set of files.')

    # required arguments (directory to check, programming language)
    parser.add_argument('-dp', '--directory-path', type=str, required=True, help='Path to the directory ' +
                        'which contains the files to check. All files from the provided directory will be checked recursively.')
    parser.add_argument('-pl', '--programming-language', type=str, required=True, help='Programming language ' +
                        'which is used in files to check. Currently only "c++" is supported.')

    # either main-sequence or distance can be displayed
    metrics_group = parser.add_mutually_exclusive_group(required=True)
    metrics_group.add_argument('-di', '--distance', action='store_true', help='Plot distance metric')
    metrics_group.add_argument('-ms', '--mainsequence', action='store_true', help='Plot Main Sequence')

    # optional argument to save plotted metrics
    parser.add_argument('-s', '--save', action='store_true', help='If true, save metric(s).')
    parser.add_argument('-sp', '--save-path', type=str, help='Optional directory path where to save the metric-file(s)')

    # parse arguments
    args = vars(parser.parse_args())

    # extract given arguments
    dir_path = args['directory_path']
    prog_lang = args['programming_language']
    show_distance = args['distance']
    show_main_sequence = args['mainsequence']
    save_metric = args['save']
    save_metric_path = args['save_path']

    # set chosen programming language
    plc.PROGRAMMING_LANGUAGE = prog_lang

    # start respective application
    if show_distance:
        dist = DistanceIA(dir_path)
        dist.plot_distance()

        # save metric if desired
        if save_metric:
            dist.save_metric(save_metric_path if save_metric_path is not None else '')

    elif show_main_sequence:
        main_seq = MainSequence(dir_path)
        main_seq.plot_metrics()

        # save metric if desired
        if save_metric:
            main_seq.save_metrics(save_metric_path if save_metric_path is not None else '')
    
    
if __name__ == '__main__':
    main()

