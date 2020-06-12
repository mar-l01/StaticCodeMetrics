import pandas as pd
import re
import warnings

import sys
sys.path.append('tests/modules_under_test/')
from utils import FileUtility, ProgrammingLanguageConfig



class AbstractnessMetric:
    def __init__(self, dir_path):
        self._dir_path = dir_path
        self._interface_class_matrix = pd.DataFrame(index=['N_a', 'N_c'], dtype=int)
        self._list_of_files = []

    def _get_number_of_interfaces_and_classes_of_file(self, file_path):  # noqa: C901
        ''' return the number of interfaces or classes present in given file.
        In C++, interfaces/abstract classes are defined using the virtual-keyword and/or one or more
        method equal to 0 (virtual void methodX() = 0;
        Info: an interface/abstract class also counts to the total amount of classes '''
        nb_interfaces = 0
        nb_classes = 0
        class_definition_found = False
        counter_namespaces = 0
        counter_curly_braces = 0

        try:
            with open(file_path, 'r') as file:
                for line in file:
                    # increment / decrement counter for curly braces
                    if '{' in line:
                        counter_curly_braces += 1

                    if '}' in line:
                        counter_curly_braces -= 1
                        # check for end of class and reset flag
                        if counter_curly_braces == counter_namespaces:
                            class_definition_found = False

                    # find namespace
                    if re.match(ProgrammingLanguageConfig.get_namespace_identifier(), line):
                        counter_namespaces += 1

                    # find class
                    if re.match(ProgrammingLanguageConfig.get_class_identifier(), line):
                        # indicate inside class definition
                        class_definition_found = True
                        nb_classes += 1

                    # find one abstract method
                    if class_definition_found:
                        if re.match(ProgrammingLanguageConfig.get_abstract_method_identifier(), line):
                            # one virtual = 0 method is sufficient for an abstract class
                            nb_interfaces += 1
                            class_definition_found = False

        except FileNotFoundError as ex:
            warnings.warn('{} ...returning default values'.format(ex))
        except ProgrammingLanguageConfig.LanguageOptionError as ex:
            warnings.warn(ex.args)

        return nb_interfaces, nb_classes

    def _search_files_for_interfaces(self):
        ''' iterate through all files and get their interfaces / abstract class definitons '''
        for file in self._list_of_files:
            nb_interfaces, nb_classes = self._get_number_of_interfaces_and_classes_of_file(file)

            # add amount of interfaces and classes to matrix
            self._interface_class_matrix[FileUtility.extract_filename(file)] = [nb_interfaces, nb_classes]

    def _calculate_abstractness_for_each_file(self):
        ''' calculate the abstractness metric using A = Na / Nc:
        0 -> no abstract classes, 1 -> only abstract classes.
        info: since it might be possible that some files do not contain any class definition at all
        each division checks for a division through zero '''
        n_a = self._interface_class_matrix.loc['N_a', :]
        n_c = self._interface_class_matrix.loc['N_c', :]

        # copy to get names in actual order, rename resulting array and change it's type accordingly
        a = n_a
        a = a.rename(index='Abstractness-Metric')
        a = a.astype(float)

        # compute abstractness metric for each row
        for index in range(len(n_a)):
            # prevent division through 0
            if n_c[index] == 0:
                a[index] = 0
            else:
                a[index] = n_a[index] / n_c[index]

        return a

    def compute_abstractness(self):
        ''' encapsulate all methods necessary to compute the abstractness values for each file:
        1) get all code file which are considered for calculating the metric
        2) extract all interfaces/abstract classed from those files
        3) calculate the abstractness metric '''
        allowed_file_extensions = []
        try:
            allowed_file_extensions = ProgrammingLanguageConfig.get_file_extensions_am()
        except ProgrammingLanguageConfig.LanguageOptionError as ex:
            warnings.warn(ex.args)

        self._list_of_files = FileUtility.get_all_code_files(self._dir_path, allowed_file_extensions)
        self._search_files_for_interfaces()
        abstractness_metric = self._calculate_abstractness_for_each_file()

        return abstractness_metric
