import unittest
import os
import filecmp
import json
import shutil
from src.internationalize.diffing_processor import compute_hashes, DiffingProcessor

class TestDiffing(unittest.TestCase):

    def setUp(self):
        self.CURR_TRANSLATION_FILES_DIR = "tests/resources/test_translations"
        self.OLD_TRANSLATIONS_ROOT_DIR = "old_translations"
        self.OLD_TRANSLATION_FILES_DIR = self.OLD_TRANSLATIONS_ROOT_DIR + "/translations"
        self.METADATA_FILE_DIR = self.OLD_TRANSLATIONS_ROOT_DIR + "/metadata.json"
        self.MODIFIED_TRANSLATIONS_DIR = "tests/resources/modified_translations"

        # initialize diffing processor
        self.dp = DiffingProcessor(self.CURR_TRANSLATION_FILES_DIR)
        self.dp.setup()

    def tearDown(self):
        if os.path.exists(self.OLD_TRANSLATIONS_ROOT_DIR):
            shutil.rmtree(self.OLD_TRANSLATIONS_ROOT_DIR)

    def test_initialization(self):
        self.assertTrue(os.path.exists(self.OLD_TRANSLATIONS_ROOT_DIR))
        self.assertTrue(os.path.exists(self.OLD_TRANSLATION_FILES_DIR))
        self.assertTrue(os.path.exists(self.METADATA_FILE_DIR))

        must_exist_files = os.listdir(self.CURR_TRANSLATION_FILES_DIR)
        match, mismatch, errors = filecmp.cmpfiles(
            self.CURR_TRANSLATION_FILES_DIR,
            self.OLD_TRANSLATION_FILES_DIR,
            must_exist_files,
            shallow=False
        )

        curr_translations_len = len(os.listdir(self.OLD_TRANSLATION_FILES_DIR))
        self.assertEqual(curr_translations_len, len(must_exist_files))
        self.assertTrue(len(match) == len(must_exist_files))
        self.assertTrue(len(mismatch) == 0)
        self.assertTrue(len(errors) == 0)

    def test_updating_state(self):
        hashes = compute_hashes(self.MODIFIED_TRANSLATIONS_DIR)
        changed_files = ["spanish.json"]
        self.dp.update_to_current_state(changed_files, hashes)

        updated_metadata = {}
        with open(self.METADATA_FILE_DIR) as file:
            updated_metadata = json.load(file)

        self.assertIsNotNone(updated_metadata["spanish"])
        self.assertIsNotNone(updated_metadata["italian"])
        self.assertEqual(hashes["spanish"], updated_metadata["spanish"])
        self.assertEqual(hashes["italian"], updated_metadata["italian"])
       
        ### Need to finish this part of test
        # must_exist_files = os.listdir(self.MODIFIED_TRANSLATIONS_DIR)
        # print(must_exist_files)
        # match, mismatch, errors = filecmp.cmpfiles(
        #     self.MODIFIED_TRANSLATIONS_DIR,
        #    self.OLD_TRANSLATION_FILES_DIR,
        #    must_exist_files,
        #    shallow=False
        # )
        # print(match)
        # self.assertTrue(len(match) == 2)

    if __name__ == '__main__':
        unittest.main()
