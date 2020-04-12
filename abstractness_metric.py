import glob
import numpy as np
import pandas as pd
import re


ALLOWED_FILE_EXTENSIONS = ['hpp', 'h']
CLASS_IDENTIFIER = '[ \t]*class[ \t\n]*;{0}'
VIRTUAL_ABSTRACT_METHOD = ['virtual', '=', '0', ';']
PATH_DELIMITER = '\\'


class AbstractnessMetric:
    def __init__(self, dir_path):
        self._dir_path = dir_path
        self._list_of_files = []

    def _create_list_of_code_files(self):
        ''' sum-up the total number of files found in the given directory '''
        for extension in ALLOWED_FILE_EXTENSIONS:
            dir_content = [file for file in glob.glob(self._dir_path + "**/*."+extension, recursive=True)]
            
            # add files of given extension to list
            self._list_of_files += [file for file in dir_content]


    def _get_interfaces_of_file(self, file_path):
        ''' return the number of interfaces present in given file.
        In C++, interfaces/abstract classes are defines using the virtual-keyword and/or one or more
        method equal to 0 (virtual void methodX() = 0;'''
        nb_interfaces = 0

        with open(file_path, 'r') as file:
            for line in file:
                if re.match(CLASS_IDENTIFIER, line):
                    print(line.strip())
                    print("Found match: {}".format(re.match(CLASS_IDENTIFIER, line)))

        return nb_interfaces
    

if __name__ == '__main__':
    directory_path = '../cppmodbus/src/cppmodbus/'
    abstractnessMetric = AbstractnessMetric(directory_path)
