import glob
from pathlib import Path
import re
import sys


# directory constants
SRC_DIR_METRICS = 'scm_modules/metrics'
SRC_DIR_UTILS = 'scm_modules/utils'
DEST_DIR_METRICS = 'tests/modules_under_test/metrics'
DEST_DIR_UTILS = 'tests/modules_under_test/utils'

# file edit constants
IMPORT_METRICS_RE = '^from scm_modules.metrics.\w+ import'  # noqa: W605
IMPORT_UTILS_RE = '^from scm_modules.utils import'  # noqa: W605
IMPORT_PATH_METRICS = 'tests/modules_under_test/metrics/'
IMPORT_PATH_UTILS = 'tests/modules_under_test/'


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


def _get_import_statements(import_definition):
    '''
    split up import-path into its different paths, e.g.
    [from] [scm_modules.utils] [import] [FileUtility, ProgrammingLanguageConfig]

    return tests/testmodules/, utils, [FileUtility, ProgrammingLanguageConfig]
    '''
    import_stmnt = import_definition.split(' ')

    # import paths are defined as point-separated module-names
    import_path = import_stmnt[1].split('.')
    import_module = import_path[-1].strip()

    # modules are appended as comma-separated list
    modules = import_stmnt[3:]

    # here: metrics import is different from utils import
    if 'metrics' in import_path:
        import_path = IMPORT_PATH_METRICS
    else:
        import_path = IMPORT_PATH_UTILS

    return import_path, import_module, modules


def _get_lines_to_add(import_path, import_module, modules):
    '''
    use provided data to return a string to be written to a file
    '''
    lines_to_add = 'import sys\n'
    lines_to_add += "sys.path.append('{}')\n".format(import_path)
    lines_to_add += "from {} import ".format(import_module)

    for module in modules:
        lines_to_add += module.strip(', ')
        lines_to_add += ', '

    # remove last ', '
    return lines_to_add.strip(', ')


def _edit_file(file_in, file_out):
    '''
    use file_in and write edited file to file_out

    find 'from scm_modules.utils import' and replace it with
        import sys
        sys.path.append('tests/modules_under_test/')
        from utils import FileUtility, ProgrammingLanguageConfig
    OR
    find 'from scm_modules.metrics.instability_metric import' replace it with:
        import sys
        sys.path.append('tests/modules_under_test/metrics/')
        from instability_metric import InstabilityMetric
    '''
    sys_already_added = False

    with open(file_in, 'r') as f_in:
        with open(file_out, 'w') as f_out:
            for line in f_in:
                # find import statements
                if re.match(IMPORT_METRICS_RE, line) or re.match(IMPORT_UTILS_RE, line):
                    # get import path and modules
                    import_path, import_module, modules = _get_import_statements(line)

                    # create altered import statements
                    altered_imports = _get_lines_to_add(import_path, import_module, modules)

                    # do not add import sys and sys.path.append() twice
                    if sys_already_added:
                        f_out.write(altered_imports.split('\n')[-2])
                    else:
                        f_out.write(altered_imports)
                        sys_already_added = True

                else:
                    f_out.write(line)


def _copy_module_files(module_files, dest_dir):
    '''
    since Python-files need to be altered before copied to new path, copying is done
    by editing and writing the file to copy to the new path
    '''
    for file in module_files:
        # __init__.py should not be considered
        if '__init__.py' not in file:
            try:
                filename = Path(file).name
                rel_file_path = Path(dest_dir).joinpath(filename)
                dest_file_path = Path.joinpath(Path.cwd().absolute(), rel_file_path)
                _edit_file(file, dest_file_path)
                print('Edited and copied file {} to directory {}..'.format(filename, dest_dir))
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
