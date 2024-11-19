import unittest
from src.internationalize.localize import Localize


class TestLocalize(unittest.TestCase):
    def setUp(self):
        # do some setting up for the tests
        pass

    def basicTest(self):
        print(Localize.translate("en", "hello"))  # Outputs the translation if found, else "Translation not found"
        print(Localize.translate("es", "hello"))  # Similarly checks Spanish language file


if __name__ == '__main__':
    unittest.main()
