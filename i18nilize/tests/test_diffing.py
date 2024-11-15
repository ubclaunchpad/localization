import unittest
import os
import filecmp
import json
import shutil
from tests.util.test_diffing_util import DiffingTestUtil
from src.internationalize.diffing_processor import compute_hashes, DiffingProcessor

class TestDiffing(unittest.TestCase):
    def setUp(self):
        self.test_translations_dir = "tests/resources/diffing_algorithm/test_translations/"
        self.basic_data_location = "tests/resources/diffing_algorithm/basic_initial_translations/"
        self.basic_modified_data_location = "tests/resources/diffing_algorithm/basic_modified_translations/"

        # initialize util class
        self.util = DiffingTestUtil(self.test_translations_dir)
        self.util.initialize_test_data(self.basic_data_location)

        # initialize diffing processor
        self.dp = DiffingProcessor(self.test_translations_dir)
        self.dp.setup()

    # tear down diffing processor instance
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


    def test_find_changed_files_basic(self):
        self.util.initialize_test_data(self.basic_modified_data_location)
        expected_changed_files = {
            "modified": ["italian.json", "spanish.json"],
            "created": ["mandarin.json"],
            "deleted": ["french.json"]
        }
        changed_files = self.dp.get_changed_files()

        for type, languages in changed_files.items():
            self.assertListEqual(languages, expected_changed_files[type])


    def test_find_changed_translations_basic(self):
        self.util.initialize_test_data(self.basic_modified_data_location)
        expected_changed_translations = expected_changed_translations = {
            "italian": {
                "type": "modified",
                "created": {},
                "modified": {
                    "thanks": "La ringrazio"
                },
                "deleted": {
                    "welcome": "benvenuto"
                }
            },
            "spanish": {
                "type": "modified",
                "created": {
                    "welcome": "bienvenido"
                },
                "modified": {
                    "hello": "holi"
                },
                "deleted": {}
            },
            "french": {
                "type": "deleted",
                "created": {},
                "modified": {},
                "deleted": {}
            },
            "mandarin": {
                "type": "created",
                "created": {
                    "hello": "ni hao",
                    "welcome": "huan yin"
                },
                "modified": {},
                "deleted": {}
            }
        }

        changed_translations = self.dp.get_changed_translations()
        self.assertEqual(changed_translations, expected_changed_translations)



    def test_updating_state(self):
        hashes = compute_hashes(self.test_translations_dir)
        changed_files = ["italian.json", "spanish.json"]
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
