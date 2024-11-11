import unittest
import os
import filecmp
import json
import shutil
from src.internationalize.diffing_processor import compute_hashes, DiffingProcessor

class TestDiffing(unittest.TestCase):

    def setUp(self):
        self.test_translations_dir = "tests/resources/test_translations"
        self.modified_translations_dir = "tests/resources/modified_translations"

        # initialize diffing processor
        self.dp = DiffingProcessor(self.test_translations_dir)
        self.dp.setup()

    def tearDown(self):
        if os.path.exists(self.dp.diff_state_root_dir):
            shutil.rmtree(self.dp.diff_state_root_dir)

    def test_initialization(self):
        self.assertTrue(os.path.exists(self.dp.diff_state_root_dir))
        self.assertTrue(os.path.exists(self.dp.diff_state_files_dir))
        self.assertTrue(os.path.exists(self.dp.metadata_file_dir))

        must_exist_files = os.listdir(self.test_translations_dir)
        match, mismatch, errors = filecmp.cmpfiles(
            self.test_translations_dir,
            self.dp.diff_state_files_dir,
            must_exist_files,
            shallow=False
        )

        curr_translations_len = len(os.listdir(self.dp.diff_state_files_dir))
        self.assertEqual(curr_translations_len, len(must_exist_files))
        self.assertTrue(len(match) == len(must_exist_files))
        self.assertTrue(len(mismatch) == 0)
        self.assertTrue(len(errors) == 0)

    def test_updating_state(self):
        hashes = compute_hashes(self.modified_translations_dir)
        changed_files = ["spanish.json"]
        self.dp.update_to_current_state(changed_files, hashes)

        updated_metadata = {}
        with open(self.dp.metadata_file_dir) as file:
            updated_metadata = json.load(file)

        self.assertIsNotNone(updated_metadata["spanish"])
        self.assertIsNotNone(updated_metadata["italian"])
        self.assertEqual(hashes["spanish"], updated_metadata["spanish"])
        self.assertEqual(hashes["italian"], updated_metadata["italian"])
       
        ### Need to finish this part of test
        # must_exist_files = os.listdir(self.modified_translations_dir)
        # print(must_exist_files)
        # match, mismatch, errors = filecmp.cmpfiles(
        #     self.modified_translations_dir,
        #    self.dp.diff_state_files_dir,
        #    must_exist_files,
        #    shallow=False
        # )
        # print(match)
        # self.assertTrue(len(match) == 2)

    if __name__ == '__main__':
        unittest.main()
