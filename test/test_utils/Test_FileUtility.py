import unittest
import warnings
import sys

sys.path.append('utils/')
import FileUtility as fut


class TestFileUtilityGetAllCodeFiles(unittest.TestCase):
    def testEmptyDirectory(self):
        '''
        Test that a valid list is returned, although
        an empty directory is provided
        '''
        returned_type = fut.get_all_code_files('', ['.h'])
        self.assertIsInstance(returned_type, list)
        self.assertEqual(returned_type, [])

    def testEmptyExtensionsList(self):
        '''
        Test that a valid list is returned, although
        an empty extensions-list is provided
        '''
        returned_type = fut.get_all_code_files('../', [])
        self.assertIsInstance(returned_type, list)
        self.assertEqual(returned_type, [])

    def testNoneListType(self):
        '''
        Test that an empty list is returned, although
        an invalid type is provided, and a warning is thrown
        '''
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")

            returned_type = fut.get_all_code_files('../', None)

            self.assertIsInstance(returned_type, list)
            self.assertEqual(returned_type, [])
            self.assertEqual(len(w), 1)
            self.assertTrue('Returning empty list..' in str(w[-1].message))


class TestFileUtilityExtractFileName(unittest.TestCase):
    def testEmptyFilePath(self):
        '''
        Test that an empty filename is returned although an empty
        filepath is given
        '''
        returned_name = fut.extract_filename('')
        self.assertEqual(returned_name, '')

    def testValidFilePath(self):
        '''
        Test that the last element is returned if a valid path is given
        '''
        valid_path = 'valid\\path\\to\\filename'
        returned_name = fut.extract_filename(valid_path)
        self.assertEqual(returned_name, 'filename')

    def testValidFilePathWrongDelimiter(self):
        '''
        Test that a wrong delimiter does return the whole filepath
        '''
        valid_path_with_wrong_delimiter = 'valid/path/to/filename'
        returned_name = fut.extract_filename(valid_path_with_wrong_delimiter)
        self.assertEqual(returned_name, 'valid/path/to/filename')


# create TestSuite with above TestCases
suite = unittest.TestSuite()
suite.addTests(unittest.makeSuite(TestFileUtilityGetAllCodeFiles))
suite.addTests(unittest.makeSuite(TestFileUtilityExtractFileName))

# run TestSuite
unittest.TextTestRunner(verbosity=2).run(suite)
