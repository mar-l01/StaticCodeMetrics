import argparse
import sys

# make main-sequence script visible
sys.path.append('metrics/')
from main_sequence import MainSequence

# init parser
parser = argparse.ArgumentParser(description='Perform static code checks on a set of files.')

# required argument (directory to check)
parser.add_argument('-dp', '--directory-path', type=str, required=True, help='Path to the directory ' + \
    'which contains the files to check. All files from the provided directory will be checked recursively.')

# parse arguments
args = vars(parser.parse_args())

# extract path given argument
dir_path = args['directory_path']

# start application
main_seq = MainSequence(dir_path)
main_seq.plot_metrics()