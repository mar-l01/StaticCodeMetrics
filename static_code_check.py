import argparse
import sys

# make main-sequence script visible
sys.path.append('metrics/')
from main_sequence import MainSequence
from distance_ia import DistanceIA

# init parser
parser = argparse.ArgumentParser(description='Perform static code checks on a set of files.')

# required argument (directory to check)
parser.add_argument('-dp', '--directory-path', type=str, required=True, help='Path to the directory ' + \
    'which contains the files to check. All files from the provided directory will be checked recursively.')

# either main-sequence or distance can be displayed
metrics_group = parser.add_mutually_exclusive_group(required=True)
metrics_group.add_argument('-di', '--distance', action='store_true')
metrics_group.add_argument('-ms', '--mainsequence', action='store_true')

# parse arguments
args = vars(parser.parse_args())

# extract path given argument
dir_path = args['directory_path']
show_distance = args['distance']
show_main_sequence = args['mainsequence']

# start respective application
if show_distance:
    dist = DistanceIA(dir_path)
    dist.plot_distance()
elif show_main_sequence:
    main_seq = MainSequence(dir_path)
    main_seq.plot_metrics()