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


def _get_module_files(src_dir):
    metrics_dir = Path.joinpath(Path.cwd().absolute(), src_dir)
    metrics_files = [file for file in glob.glob(str(metrics_dir) + '**/*.py', recursive=True)]

    return metrics_files


def _copy_module_files(module_files, dest_dir):
    for file in module_files:
        # __init__.py should not be considered
        if '__init__.py' not in file:
            try:
                filename = file.split(DELIMITER)[-1]
                dest_file_path = Path.joinpath(Path.cwd().absolute(), dest_dir + DELIMITER + filename)
                shutil.copyfile(file, dest_file_path)
                print('Copied file {} to directory {}..'.format(filename, dest_dir))
            except Exception as ex:
                print('Failed to copy file {} to directory {} with error {}!'.format(file, dest_dir, ex))
                return 1
    
    return 0


def _copy_files():
    metrics_files = _get_module_files(SRC_DIR_METRICS)
    utils_files = _get_module_files(SRC_DIR_UTILS)
    
    if _copy_module_files(metrics_files, DEST_DIR_METRICS) or _copy_module_files(utils_files, DEST_DIR_UTILS):
        return 1
    
    return 0


if __name__ == '__main__':
    if _create_env() == 1:
        sys.exit(1)

    # try to copy all files
    error_code = _copy_files()
    sys.exit(error_code)
