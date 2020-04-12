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


    def _create_two_dim_data_frame(self):
        ''' create a 2D matrix with the given size (typically dim = m x m).
        if standard-library includes are used, too, dim = m x n, with n > m'''
        m = len(self._list_of_files)

        # compute n if std-library includes are used
        if self._use_std_includes:
            pass
        
        null_matrix = np.zeros((m, m), dtype=int)
        names = [self._get_filename(filepath) for filepath in self._list_of_files]
        self._data_frame = pd.DataFrame(null_matrix, index=names, columns=names)


    def _get_filename(self, filepath):
        ''' return solely the filename including the extension '''
        # get last part of file_path
        filename = filepath.split(PATH_DELIMITER)[-1]

        return filename


    def _fill_matrix(self):
        ''' fill matrix by setting np_matrix[x,y] to 1 if x includes y '''
        # check includes
        for filepath in self._list_of_files:
            # get filename which includes following files
            including_file = self._get_filename(filepath)

            self._get_interfaces_of_file(filepath)


    def _get_all_fan_in(self):
        ''' uses provided data frame to evaluate the fan-in's of each file (:= #1's in row) '''
        return np.sum(self._data_frame, axis=1)


    def _get_all_fan_out(self):
        ''' uses provided data frame to evaluate the fan-out's of each file (:= #1's in column) '''
        return np.sum(self._data_frame, axis=0)


    def _calculate_instability_for_each_file(self):
        ''' calculate the instability metric using I = fan_out / (fan_in + fan_out)
            1 -> unstable, 0 -> stable '''
        fan_in = self._get_all_fan_in()
        fan_out = self._get_all_fan_out()
        i = fan_out / (fan_in + fan_out)

        return i

    def compute_instability(self):
        ''' encapsulate all methods necessary to compute the instability values for each component '''
        self._create_list_of_code_files()
        #self._create_two_dim_data_frame()
        self._fill_matrix()
    

if __name__ == '__main__':
    #directory_path = 'C:/Users/Markus/Documents/Programmieren/C++Tutorial'
    directory_path = 'C:/Users/Markus/Desktop/cppmodbus/src/cppmodbus/'
    abstractnessMetric = AbstractnessMetric(directory_path)
    abstractnessMetric.compute_instability()
