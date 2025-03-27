import filecmp
import logging
import os
import shutil
import unittest

from src.internationalize import globals
from src.internationalize.diffing_processor import (
    DiffingProcessor,
    compute_hashes,
    read_json_file,
)
from tests.util.test_diffing_util import DiffingTestUtil


class TestDiffing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)
        logging.getLogger("dirsync").disabled = True

        # 'mock' translations folder to mimic real user interaction
        cls.test_translations_dir = os.path.join(
            "tests", "resources", "diffing_algorithm", "test_translations"
        )

        # main directory for diffing tests
        cls.test_data_location = os.path.join(
            "tests", "resources", "diffing_algorithm", "all_tests"
        )

        # standardized names for a test folder
        cls.initial_translations_dir = "initial_translations"
        cls.modified_translation_dir = "modified_translations"
        cls.expected_output_file = "expected_output.json"

        # default test data to basic tests
        cls.basic_initial_data_location = cls.get_test_path(
            "basic_test", cls.initial_translations_dir
        )
        cls.basic_modified_data_location = cls.get_test_path(
            "basic_test", cls.modified_translation_dir
        )
        cls.basic_expected_output = cls.get_test_path(
            "basic_test", cls.expected_output_file
        )

        # initialize classes
        cls.util = DiffingTestUtil(cls.test_translations_dir)
        cls.dp = DiffingProcessor(cls.test_translations_dir)

        return super().setUpClass()

    def setUp(self):
        globals.ROOT_DIRECTORY = "test_directory__do_not_commit"
        globals.LANGUAGES_DIR = os.path.join(globals.ROOT_DIRECTORY, "languages")
        os.makedirs(globals.LANGUAGES_DIR, exist_ok=True)

        # initialize util class
        self.util.initialize_test_data(self.basic_initial_data_location)

        # initialize diffing processor
        self.dp.setup(create_ms_token=False)

    # tear down diffing folder
    def tearDown(self):
        if os.path.exists(self.dp.diff_state_root_dir):
            shutil.rmtree(self.dp.diff_state_root_dir)

        if os.path.exists(globals.ROOT_DIRECTORY):
            shutil.rmtree(globals.ROOT_DIRECTORY)

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
            shallow=False,
        )

        curr_translations_len = len(os.listdir(self.dp.diff_state_files_dir))
        self.assertEqual(curr_translations_len, len(must_exist_files))
        self.assertTrue(len(match) == len(must_exist_files))
        self.assertTrue(len(mismatch) == 0)
        self.assertTrue(len(errors) == 0)

    def test_updating_state(self):
        new_hashes = compute_hashes(self.basic_modified_data_location)
        self.util.initialize_test_data(self.basic_modified_data_location)
        self.dp.update_to_current_state(new_hashes)
        modified_metadata = read_json_file(self.dp.metadata_file_dir)
        self.assertEqual(new_hashes, modified_metadata)

    def test_no_updates_to_state(self):
        hashes = compute_hashes(self.basic_initial_data_location)
        self.util.initialize_test_data(self.basic_initial_data_location)
        self.dp.update_to_current_state(hashes)
        same_metadata = read_json_file(self.dp.metadata_file_dir)
        self.assertEqual(hashes, same_metadata)

    def test_synchronization(self):
        # Remove initial translations
        if os.path.exists(self.dp.diff_state_files_dir):
            shutil.rmtree(self.dp.diff_state_files_dir)
        os.mkdir(self.dp.diff_state_files_dir)

        curr_state_files = os.listdir(self.dp.curr_translation_files_dir)
        old_state_files = os.listdir(self.dp.diff_state_files_dir)
        self.assertEqual(len(curr_state_files), 4)
        self.assertEqual(len(old_state_files), 0)

        self.dp.sync_translations()
        modified_old_state_files = os.listdir(self.dp.diff_state_files_dir)
        self.assertEqual(len(modified_old_state_files), 4)

    def test_find_changed_files_basic(self):
        self.util.initialize_test_data(self.basic_modified_data_location)
        expected_changed_files = {
            "modified": ["italian.json", "spanish.json"],
            "created": ["mandarin.json"],
            "deleted": ["french.json"],
        }
        changed_files = self.dp.get_changed_files()

        for type, languages in changed_files.items():
            self.assertCountEqual(
                languages, expected_changed_files[type], f"Mismatch in {type} files"
            )

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
        initial_data_location = self.get_test_path(
            test_name, self.initial_translations_dir
        )
        modified_data_location = self.get_test_path(
            test_name, self.modified_translation_dir
        )
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


if __name__ == "__main__":
    unittest.main()
