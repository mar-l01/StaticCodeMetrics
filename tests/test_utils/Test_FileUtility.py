import pandas as pd
from pathlib import Path
import unittest
from unittest.mock import patch
import warnings
import sys

sys.path.append('tests/modules_under_test/utils/')
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


class TestFileUtilitySaveMetricToFile(unittest.TestCase):
    @patch('pathlib.Path.is_dir')
    @patch('pathlib.Path.mkdir')
    @patch('pathlib.Path.joinpath')
    @patch('pandas.Series.to_csv')
    def testSaveIfEmptyDirectory(self, mocked_pd_csv, mocked_pl_join, mocked_pl_mkdir, mocked_pl_isdir):
        '''
        Test that metric is saved correctly with an empty directory path given
        '''
        # assert mocks
        self.assertIs(pd.Series.to_csv, mocked_pd_csv)
        self.assertIs(Path.mkdir, mocked_pl_mkdir)
        self.assertIs(Path.joinpath, mocked_pl_join)
        self.assertIs(Path.is_dir, mocked_pl_isdir)

        # create mock values
        mocked_metric = pd.Series([.1, .2, .3], name='metric-mock', dtype=float)
        mocked_pl_isdir.return_value = False  # create default directory
        mocked_pl_join.return_value = Path('default/directory/file')

        # call function to test
        fut.save_metric_to_file(mocked_metric)  # save to default directory

        # assert calls
        mocked_pl_isdir.assert_called()  # called twice
        mocked_pl_mkdir.assert_called_once()
        mocked_pl_join.assert_called()  # called twice
        mocked_pd_csv.assert_called_once()

    @patch('pathlib.Path.is_dir')
    @patch('pathlib.Path.joinpath')
    @patch('pandas.Series.to_csv')
    def testSaveIfExistingDirectory(self, mocked_pd_csv, mocked_pl_join, mocked_pl_isdir):
        '''
        Test that metric is saved correctly given an existing directory path
        '''
        # assert mocks
        self.assertIs(pd.Series.to_csv, mocked_pd_csv)
        self.assertIs(Path.joinpath, mocked_pl_join)
        self.assertIs(Path.is_dir, mocked_pl_isdir)

        # create mock values
        mocked_metric = pd.Series([.1, .2, .3], name='metric-mock', dtype=float)
        mocked_pl_isdir.return_value = True  # given directory given
        mocked_pl_join.return_value = Path('default/directory/file')

        # call function to test
        fut.save_metric_to_file(mocked_metric, 'dummy/directory')

        # assert calls
        mocked_pl_isdir.assert_called_once()
        mocked_pl_join.assert_called_once()
        mocked_pd_csv.assert_called_once()
