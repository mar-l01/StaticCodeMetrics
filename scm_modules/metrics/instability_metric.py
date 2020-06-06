import numpy as np
import pandas as pd
import warnings

from scm_modules.utils import FileUtility, ProgrammingLanguageConfig as plc


class InstabilityMetric:
    def __init__(self, dir_path):
        self._dir_path = dir_path
        self._list_of_user_files = []
        self._include_matrix = pd.DataFrame()

    def _get_includes_of_file(self, file_path):
        ''' return the files included with #include "..." and #include <...> in provided file
        in two separated arrays, one for user-includes and one for stl-includes '''
        user_include_list = []
        stl_include_list = []

        try:
            with open(file_path, 'r') as file:
                for line in file:
                    if line.startswith(ProgrammingLanguageConfig.get_prefix_user_include_identifier()):
                        # ignore ending " to get the pure filename
                        include_filename =
                            line[len(ProgrammingLanguageConfig.get_prefix_user_include_identifier()):].strip()[:-1]
                        user_include_list.append(include_filename)
                    elif line.startswith(ProgrammingLanguageConfig.get_prefix_standard_include_identifier()):
                        # ignore ending > to get the pure filename
                        include_filename =
                            line[len(ProgrammingLanguageConfig.get_prefix_standard_include_identifier()):].strip()[:-1]
                        stl_include_list.append(include_filename)

        except FileNotFoundError as ex:
            warnings.warn('{} ...returning default values'.format(ex))
        except ProgrammingLanguageConfig.LanguageOptionError as ex:
            warnings.warn(ex.args)

        return user_include_list, stl_include_list

    def _create_user_include_matrix(self):
        ''' create a 2D matrix with dim = m x n, where m is the number of user-included files '''
        m = len(self._list_of_user_files)
        null_matrix = np.zeros((m, m), dtype=int)
        names = [FileUtility.extract_filename(filepath) for filepath in self._list_of_user_files]
        self._include_matrix = pd.DataFrame(null_matrix, index=names, columns=names)

    def _fill_include_matrix(self):
        ''' fill matrix by setting matrix[x,y] to 1 if x includes y for all user-included files, which
        are indicated by #include "...". Additonally, stl-included files are also handled '''
        # check includes
        for filepath in self._list_of_user_files:
            # get filename which includes the following files
            including_file = FileUtility.extract_filename(filepath)

            # get list of user-includes
            user_includes, stl_includes = self._get_includes_of_file(filepath)

            # #include "..." usage, fill 1 if needed (row=including_file, column=user_included_file)
            for user_included_file in user_includes:
                self._include_matrix.at[including_file, user_included_file] = 1

            # #include <...> usage, fill 1 if needed (row=including_file, column=stl_included_file)
            for stl_included_file in stl_includes:
                self._include_matrix.at[including_file, stl_included_file] = 1

    def _add_stl_includes(self):
        ''' In order to be able to handle included stl-files, each time an including_file includes stl-files
        (indicated by #include <...>), they are added to a member-list '''
        self._list_of_stl_libs = []

        # check includes
        for filepath in self._list_of_user_files:
            # get list of stl-includes
            _, stl_includes = self._get_includes_of_file(filepath)

            # #include <...> usage, add stl-files to global list
            for stl_included_file in stl_includes:
                self._list_of_stl_libs.append(stl_included_file)

        # remove duplicates of global stl-files list
        self._list_of_stl_libs = list(set(self._list_of_stl_libs))

        for stl_included_file in self._list_of_stl_libs:
            self._include_matrix.loc[:, stl_included_file] = pd.Series(np.zeros(len(self._include_matrix.index)), dtype=int)

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
        i = i.rename(index='Instability-Metric')
        i = i.astype(float)

        # compute instability metric for each row
        for index in range(len(fan_in)):
            # prevent division through 0
            if fan_out[index] == 0 and fan_in[index] == 0:
                i[index] = 0
            else:
                i[index] = fan_out[index] / (fan_in[index] + fan_out[index])

        return i

    def compute_instability(self):
        ''' encapsulate all methods necessary to compute the instability values for each component '''
        allowed_file_extensions = []
        try:
            allowed_file_extensions = ProgrammingLanguageConfig.get_file_extensions_im()
        except ProgrammingLanguageConfig.LanguageOptionError as ex:
            warnings.warn(ex.args)

        self._list_of_user_files = FileUtility.get_all_code_files(self._dir_path, allowed_file_extensions)
        self._create_user_include_matrix()
        self._add_stl_includes()
        self._fill_include_matrix()
        instability_metric = self._calculate_instability_for_each_file()

        return instability_metric
