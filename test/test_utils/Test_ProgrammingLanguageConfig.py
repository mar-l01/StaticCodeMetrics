import unittest
import sys

sys.path.append('utils/')
import ProgrammingLanguageConfig as plc
import ProgrammingLanguageConstants as plconst


class TestProgrammingLanguageConfigAllGetterMethodsCPP(unittest.TestCase):
    def setUp(self):
        '''
        Set programming language to C++
        '''
        plc.PROGRAMMING_LANGUAGE = 'c++'

    def testGetFileExtensionsIm(self):
        '''
        Test that a correct C++ file exentsions for instability metric are returned
        '''
        returned_file_extensions = plc.get_file_extensions_im()
        self.assertEqual(returned_file_extensions, plconst.CPP_ALLOWED_FILE_EXTENSIONS_IM)

    def testGetFileExtensionsAm(self):
        '''
        Test that a correct C++ file exentsions for abstractness metric are returned
        '''
        returned_file_extensions = plc.get_file_extensions_am()
        self.assertEqual(returned_file_extensions, plconst.CPP_ALLOWED_FILE_EXTENSIONS_AM)

    def testGetClassIdentifier(self):
        '''
        Test that a correct C++ class identifier (regex) is returned
        '''
        returned_class_identifier = plc.get_class_identifier()
        self.assertEqual(returned_class_identifier, plconst.CPP_CLASS_IDENTIFIER)

    def testGetInterfaceIdentifier(self):
        '''
        Test that a exceptioni is thrown because C++ does not provide an interface identifier
        '''
        try:
            plc.get_interface_identifier()
        except Exception as ex:
            self.assertTrue('C++ does not have an interface identifier' in str(ex))

    def testGetAbstractMethodIdentifier(self):
        '''
        Test that a correct C++ abstract method identifier (regex) is returned
        '''
        returned_abstract_method_identifer = plc.get_abstract_method_identifier()
        self.assertEqual(returned_abstract_method_identifer, plconst.CPP_ABSTRACT_METHOD_IDENTIFIER)

    def testGetNamespaceIdentifier(self):
        '''
        Test that a correct C++ namespace identifier (regex) is returned
        '''
        returned_namespace_identifier = plc.get_namespace_identifier()
        self.assertEqual(returned_namespace_identifier, plconst.CPP_NAMESPACE_IDENTIFIER)

    def testGetPrefixUserIncludeIdentifier(self):
        '''
        Test that a correct C++ user include prefix is returned
        '''
        returned_user_include_identifier = plc.get_prefix_user_include_identifier()
        self.assertEqual(returned_user_include_identifier, plconst.CPP_PREFIX_USER_INCLUDE)

    def testGetPrefixStandardIncludeIdentifier(self):
        '''
        Test that a correct C++ standard include prefix is returned
        '''
        returned_std_include_identifier = plc.get_prefix_standard_include_identifier()
        self.assertEqual(returned_std_include_identifier, plconst.CPP_PREFIX_STD_INCLUDE)
