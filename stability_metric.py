import glob
import numpy as np
import pandas as pd


ALLOWED_FILE_EXTENSIONS = ['cpp', 'hpp', 'c', 'h']
PREFIX_STD_INCLUDE = '#include <'
PREFIX_USER_INCLUDE = '#include "'
PATH_DELIMITER = '\\'


class StabilityMetric:
    def __init__(self, dir_path):
        self._dir_path = dir_path
        self._list_of_user_files = []
        self._list_of_stl_libs = []

    def _create_list_of_code_files(self):
        ''' sum-up the total number of code-files (header and source) found in the given directory '''
        for extension in ALLOWED_FILE_EXTENSIONS:
            dir_content = [file for file in glob.glob(self._dir_path + "**/*."+extension, recursive=True)]
            
            # add files of given extension to list
            self._list_of_user_files += [file for file in dir_content]


    def _get_includes_of_file(self, file_path):
        ''' return the files included with #include "..." and #include <...> in provided file
        in two separated arrays, one for user-includes and one for stl-includes '''
        user_include_list = []
        stl_include_list = []

        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith(PREFIX_USER_INCLUDE):
                    # ignore ending " to get the pure filename
                    include_filename = line[len(PREFIX_USER_INCLUDE):].strip()[:-1]
                    user_include_list.append(include_filename)
                elif line.startswith(PREFIX_STD_INCLUDE):
                    # ignore ending > to get the pure filename
                    include_filename = line[len(PREFIX_STD_INCLUDE):].strip()[:-1]
                    stl_include_list.append(include_filename)

        return user_include_list, stl_include_list
    

    def _create_user_include_matrix(self):
        ''' create a 2D matrix with dim = m x n, where m is the number of user-included files '''
        m = len(self._list_of_user_files)
        null_matrix = np.zeros((m, m), dtype=int)
        names = [self._get_filename(filepath) for filepath in self._list_of_user_files]
        self._include_matrix = pd.DataFrame(null_matrix, index=names, columns=names)
        

    def _get_filename(self, filepath):
        ''' return solely the filename including the extension '''
        # get last part of file_path
        filename = filepath.split(PATH_DELIMITER)[-1]

        return filename


    def _fill_include_matrix(self):
        ''' fill matrix by setting matrix[x,y] to 1 if x includes y for all user-included files, which
        are indicated by #include "...". Additonally, stl-included files are also handled '''        
        # check includes
        for filepath in self._list_of_user_files:
            # get filename which includes the following files
            including_file = self._get_filename(filepath)

            # get list of user-includes
            user_includes, stl_includes = self._get_includes_of_file(filepath)

            # #include "..." usage, fill 1 if needed (row=including_file, column=user_included_file)
            for user_included_file in user_includes:
                self._include_matrix.at[including_file , user_included_file] = 1

            # #include <...> usage, fill 1 if needed (row=including_file, column=stl_included_file)
            for stl_included_file in stl_includes:
                self._include_matrix.at[including_file , stl_included_file] = 1


    def _add_stl_includes(self):
        ''' In order to be able to handle included stl-files, each time an including_file includes stl-files
        (indicated by #include <...>), they are added to a member-list '''        
        # check includes
        for filepath in self._list_of_user_files:
            # get filename which includes the following files
            including_file = self._get_filename(filepath)

            # get list of stl-includes
            _, stl_includes = self._get_includes_of_file(filepath)
            
            # #include <...> usage, add stl-files to global list
            for stl_included_file in stl_includes:
                self._list_of_stl_libs.append(stl_included_file)

        # remove duplicates of global stl-files list 
        self._list_of_stl_libs = list(set(self._list_of_stl_libs))


    def _get_all_fan_in(self):
        ''' uses provided data frame to evaluate the fan-in's of each file (:= #1's in row) '''
        return np.sum(self._include_matrix, axis=1)


    def _get_all_fan_out(self):
        ''' uses provided data frame to evaluate the fan-out's of each file (:= #1's in column) '''
        return np.sum(self._include_matrix, axis=0)


    def _calculate_instability_for_each_file(self):
        ''' calculate the instability metric using I = fan_out / (fan_in + fan_out):
        1 -> unstable, 0 -> stable.
        info: fan_in might contain less values than fan_out due to the included stl-files, and hence
        each row has its counterpart in the columns for shape m x m, if index(column) > m the symmetry
        broken '''
        fan_in = self._get_all_fan_in()
        fan_out = self._get_all_fan_out()

        # copy to get names in actual order
        i = fan_in

        # compute instability metrix for each row
        for index, row in enumerate(fan_in):
            i[index] = fan_out[index] / (row + fan_out[index]) 

        return i

    def compute_instability(self):
        ''' encapsulate all methods necessary to compute the instability values for each component '''
        self._create_list_of_code_files()
        self._create_user_include_matrix()
        self._add_stl_includes()
        self._fill_include_matrix()

        instability_metric = self._calculate_instability_for_each_file()
        print("---------- INSTABILITY ----------")
        print(instability_metric)
        print("---------------------------------")
    

if __name__ == '__main__':
    directory_path = '../cppmodbus/src/cppmodbus/'
    stabilityMetric = StabilityMetric(directory_path)
    stabilityMetric.compute_instability()
