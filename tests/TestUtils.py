import unittest
import warnings
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

    def test__get_all_code_files__None_list_type(self):
        '''
        Test that an empty list is returned, although
        an invalid type is provided, and a warning is thrown
        '''
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")

            returned_type = fut.get_all_code_files('../', None)
            self.assertIsInstance(returned_type, list)
            
            assert len(w) == 1
            assert 'Returning empty list..' in str(w[-1].message)

    


if __name__ == '__main__':
    unittest.main()
