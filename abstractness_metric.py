import glob
import numpy as np
import pandas as pd
import re


ALLOWED_FILE_EXTENSIONS = ['hpp', 'h']
PATH_DELIMITER = '\\'

# [\w()]* handles the __ declspec(dllexport)-part of class definition:
# e.g. class __declspec(dllexport) ModbusTcpClient
CLASS_IDENTIFIER = '\s*(class|struct)\s*[\w()]*\s*\w+\s*'

# abstract methods in C++ are typically denoted by setting a virtual method equal to 0:
# e.g. virtual void anAbstractMethod() = 0;
# it start with (virtual) and ends with (= 0;)
ABSTRACT_METHOD_IDENTIFIER = '^(\s*virtual)\s+\w+\s*\w*\((.|\s)*\)\s*(=\s*0\s*;)$'

# namespaces are indicated by namespace namespaceX
NAMESPACE_IDENTIFIER = '^(\s*namespace)\s*\w*\s*'


class AbstractnessMetric:
    def __init__(self, dir_path):
        self._dir_path = dir_path
        self._list_of_files = []
        self._interface_class_matrix = pd.DataFrame(index=['N_a', 'N_c'], dtype=int)

    def _create_list_of_code_files(self):
        ''' sum-up the total number of header-files, containing the class definition, found in the given directory '''
        for extension in ALLOWED_FILE_EXTENSIONS:
            dir_content = [file for file in glob.glob(self._dir_path + "**/*."+extension, recursive=True)]
            
            # add files of given extension to list
            self._list_of_files += [file for file in dir_content]


    def _get_number_of_interfaces_and_classes_of_file(self, file_path):
        ''' return the number of interfaces or classes present in given file.
        In C++, interfaces/abstract classes are defined using the virtual-keyword and/or one or more
        method equal to 0 (virtual void methodX() = 0;
        Info: an interface/abstract class also counts to the total amount of classes '''
        nb_interfaces = 0
        nb_classes = 0
        class_definition_found = False
        counter_namespaces = 0
        counter_curly_braces = 0

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
                if re.match(NAMESPACE_IDENTIFIER, line):
                    counter_namespaces += 1
                    
                # find class
                if re.match(CLASS_IDENTIFIER, line):
                    # indicate inside class definition
                    class_definition_found = True
                    nb_classes += 1
                    
                # find one abstract method
                if class_definition_found:
                    if re.match(ABSTRACT_METHOD_IDENTIFIER, line):
                        # one virtual = 0 method is sufficient for an abstract class
                        nb_interfaces += 1
                        class_definition_found = False

        return nb_interfaces, nb_classes


    def _get_filename(self, filepath):
        ''' return solely the filename including the extension '''
        # get last part of file_path
        filename = filepath.split(PATH_DELIMITER)[-1]

        return filename


    def _search_files_for_interfaces(self):
        ''' iterate through all files and get their interfaces / abstract class definitons '''
        nb_interfaces_in_files = 0
        nb_classes_in_files = 0
        
        for file in self._list_of_files:
            nb_interfaces, nb_classes = self._get_number_of_interfaces_and_classes_of_file(file)

            nb_interfaces_in_files += nb_interfaces
            nb_classes_in_files += nb_classes

            # add amount of interfaces and classes to matrix
            self._interface_class_matrix[self._get_filename(file)] = [nb_interfaces, nb_classes]


    def _calculate_abstractness_for_each_file(self):
        ''' calculate the abstractness metric using A = Na / Nc:
        0 -> no abstract classes, 1 -> only abstract classes.
        info: sicne it might be possible that some files do not contain any class definition at all
        each division checks for a division through zero '''
        n_a = self._interface_class_matrix.loc['N_a', :]
        n_c = self._interface_class_matrix.loc['N_c', :]

        # copy to get names in actual order and rename resulting array
        a = n_a
        a = a.rename(index='Abstractness-Metric')

        # compute instability metrix for each row
        for index in range(len(n_a)):
            # prevent division through 0
            if n_c[index] == 0:
                a[index] = 0
            else:
                a[index] = n_a[index] / n_c[index]

        print(a)

        return a


    def compute_abstractness(self):
        ''' encapsulate all methods necessary to compute the abstractness values for each file '''
        self._create_list_of_code_files()
        self._search_files_for_interfaces()
        self._calculate_abstractness_for_each_file()
    

if __name__ == '__main__':
    directory_path = '../cppmodbus/src/cppmodbus/'
    abstractnessMetric = AbstractnessMetric(directory_path)
    abstractnessMetric.compute_abstractness()
