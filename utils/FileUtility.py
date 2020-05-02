from datetime import datetime
import glob
import pandas as pd
from pathlib import Path
import warnings

# glob extends paths with \
PATH_DELIMITER = '\\'

# default directory for saved metric
DEFAULT_DIRECTORY = 'saved_metrics'


def get_all_code_files(directory_path, allowed_file_extensions):
    ''' return a list containing all files with the provided file-extension(s) found in the given directory '''
    code_files = []

    # check that 2nd parameter is of type list, if not return empty list
    if not isinstance(allowed_file_extensions, list):
        warnings.warn('"allowed_file_extensions" is not of required type list. Returning empty list..')
        return code_files

    for extension in allowed_file_extensions:
        directory_content = [file for file in glob.glob(directory_path + "**/*." + extension, recursive=True)]

        # add files of given extension to list
        code_files += [file for file in directory_content]

    return code_files


def extract_filename(filepath):
    ''' return solely the filename including the extension '''
    # get last part of file_path
    filename = filepath.split(PATH_DELIMITER)[-1]

    return filename


def save_metric_to_file(metric, directory_path=''):
    ''' save given metric to given directory-path. Use (and create) default directory if it does not exist '''
    # use default directory if provided path does not exist
    if not Path(directory_path).is_dir() or directory_path == '':
        directory_path = Path.joinpath(Path.cwd().absolute(), DEFAULT_DIRECTORY)

        # create default directory if not already existing
        if not Path(directory_path).is_dir():
            Path(directory_path).mkdir(parents=True, exist_ok=True)
    else:
        # create Path object otw.
        directory_path = Path(directory_path)

    filename = '{}_{}.csv'.format(metric.name.lower(), datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    filepath = Path.joinpath(directory_path, filename)
    metric.to_csv(filepath)
