import glob
from pathlib import Path
import shutil
import sys

# constants
DELIMITER = '\\'

# directory constants
SRC_DIR_METRICS = 'scm_modules/metrics'
SRC_DIR_UTILS = 'scm_modules/utils'
DEST_DIR_METRICS = 'tests/testmodules/metrics'
DEST_DIR_UTILS = 'tests/testmodules/utils'


def _create_env():
    if not Path(SRC_DIR_METRICS).is_dir() or not Path(SRC_DIR_UTILS).is_dir():
        return 1

    if not Path(DEST_DIR_METRICS).is_dir():
        Path(DEST_DIR_METRICS).mkdir(parents=True, exist_ok=True)

    if not Path(DEST_DIR_UTILS).is_dir():
        Path(DEST_DIR_UTILS).mkdir(parents=True, exist_ok=True)

    return 0


def _get_metrics_files():
    metrics_dir = Path.joinpath(Path.cwd().absolute(), SRC_DIR_METRICS)
    metrics_files = [file for file in glob.glob(str(metrics_dir) + '**/*.py', recursive=True)]

    return metrics_files


def _get_utils_files():
    utils_dir = Path.joinpath(Path.cwd().absolute(), SRC_DIR_UTILS)
    utils_files = [file for file in glob.glob(str(utils_dir) + '**/*.py', recursive=True)]

    return utils_files



def _copy_files():
    metrics_files = _get_metrics_files()
    utils_files = _get_utils_files()

    for m_file in metrics_files:
        # __init__.py should not be considered
        if not '__init__.py' in m_file:
            try:
                filename = m_file.split(DELIMITER)[-1]
                dest_file_path = Path.joinpath(Path.cwd().absolute(), DEST_DIR_METRICS + DELIMITER + filename)
                shutil.copyfile(m_file, dest_file_path)
                print('Copied file {} to directory {}..'.format(filename, DEST_DIR_METRICS))
            except Exception as ex:
                print('Failed to copy file {} to directory {}'.format(m_file, DEST_DIR_METRICS))
                return 1

    for u_file in utils_files:
        # __init__.py should not be considered
        if not '__init__.py' in u_file:
            try:
                filename = u_file.split(DELIMITER)[-1]
                dest_file_path = Path.joinpath(Path.cwd().absolute(), DEST_DIR_UTILS + DELIMITER + filename)
                shutil.copyfile(u_file, dest_file_path)
                print('Copied file {} to directory {}..'.format(filename, DEST_DIR_UTILS))
            except Exception as ex:
                print('Failed to copy file {} to directory {}'.format(u_file, DEST_DIR_UTILS))
                return 1

    return 0


if __name__ == '__main__':
    if _create_env() == 1:
        sys.exit(1)

    # try to copy all files
    error_code = _copy_files()
    sys.exit(error_code)
