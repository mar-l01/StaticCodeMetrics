import unittest
import sys

# make utility scripts visible
sys.path.append('../utils/')
import FileUtility as fut


class TestFileUtility(unittest.TestCase):
    def test__get_all_code_files__empty_directory(self):
        '''
        Test that a valid list is returned, although
        an empty directory is provided
        '''
        returned_type = fut.get_all_code_files('', ['.h'])
        self.assertIsInstance(returned_type, list)

    def test__get_all_code_files__empty_extensions_list(self):
        '''
        Test that a valid list is returned, although
        an empty extensions-list is provided
        '''
        returned_type = fut.get_all_code_files('../', [])
        self.assertIsInstance(returned_type, list)

if __name__ == '__main__':
    unittest.main()
