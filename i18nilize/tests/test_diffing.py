import logging
import unittest
import os
import filecmp
import json
import shutil
from tests.util.test_diffing_util import DiffingTestUtil
from src.internationalize.diffing_processor import compute_hashes, read_json_file, DiffingProcessor

class TestDiffing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)

        # 'mock' translations folder to mimic real user interaction
        cls.test_translations_dir = "tests/resources/diffing_algorithm/test_translations"

        # main directory for diffing tests
        cls.test_data_location = "tests/resources/diffing_algorithm/all_tests"

        # standardized names for a test folder
        cls.initial_translations_dir = "initial_translations"
        cls.modified_translation_dir = "modified_translations"
        cls.expected_output_file = "expected_output.json"

        # default test data to basic tests
        cls.basic_initial_data_location = cls.get_test_path("basic_test", cls.initial_translations_dir)
        cls.basic_modified_data_location = cls.get_test_path("basic_test", cls.modified_translation_dir)
        cls.basic_expected_output = cls.get_test_path("basic_test", cls.expected_output_file)

        # initialize classes
        cls.util = DiffingTestUtil(cls.test_translations_dir)
        cls.dp = DiffingProcessor(cls.test_translations_dir)

        return super().setUpClass()

    def setUp(self):
        # initialize util class
        self.util.initialize_test_data(self.basic_initial_data_location)

        # initialize diffing processor
        self.dp.setup()

    # tear down diffing folder
    def tearDown(self):
        if os.path.exists(self.dp.diff_state_root_dir):
            shutil.rmtree(self.dp.diff_state_root_dir)

    # remove redundant folder after testing
    @classmethod
    def tearDownClass(cls):
        cls.util.clear_test_data()
        return super().tearDownClass()

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

    def test_find_changed_files_basic(self):
        self.util.initialize_test_data(self.basic_modified_data_location)
        expected_changed_files = {
            "modified": ["italian.json", "spanish.json"],
            "created": ["mandarin.json"],
            "deleted": ["french.json"]
        }
        changed_files = self.dp.get_changed_files()

        for type, languages in changed_files.items():
            self.assertListEqual(languages, expected_changed_files[type], f"Mismatch in {type} files")

    def test_bulk_find_changed_translations(self):
        for test_folder in os.listdir(self.test_data_location):
            with self.subTest(test_folder=test_folder):
                self.run_single_changed_translation_test(test_folder)

    def run_single_changed_translation_test(self, test_name):
        logging.info("\n\n" + "-" * 40)
        logging.info(f"Running test: {test_name}")

        # clear diff directory
        if os.path.exists(self.dp.diff_state_root_dir):
            shutil.rmtree(self.dp.diff_state_root_dir)

        # Set test directories
        initial_data_location = self.get_test_path(test_name, self.initial_translations_dir)
        modified_data_location = self.get_test_path(test_name, self.modified_translation_dir)
        expected_output = self.get_test_path(test_name, self.expected_output_file)

        # Initialize translations
        self.util.initialize_test_data(initial_data_location)
        self.dp.setup()

        # Modify translations
        self.util.initialize_test_data(modified_data_location)
        expected_changed_translations = read_json_file(expected_output)

        changed_translations = self.dp.get_changed_translations()
        try:
            self.assertEqual(changed_translations, expected_changed_translations)
        except Exception as e:
            logging.info(f"test {test_name} failed!: {e}") 
            logging.info("\n" + "-" * 40 + "\n")
            raise

        logging.info(f"Test passed: {test_name}")
        logging.info("\n" + "-" * 40 + "\n")

    @classmethod
    def get_test_path(cls, test_name, folder_type):
        return os.path.join(cls.test_data_location, test_name, folder_type)


if __name__ == '__main__':
    unittest.main()
