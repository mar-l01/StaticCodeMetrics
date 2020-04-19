import glob
import warnings

# glob extends paths with \
PATH_DELIMITER = '\\'


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
