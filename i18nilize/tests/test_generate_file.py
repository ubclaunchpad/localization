import unittest
from src.internationalize.helpers import get_json, generate_file

# run tests using python -m tests.test_generate_file at i18nilize directory level

class TestGenerateFile(unittest.TestCase):
    generate_file()
    data = get_json("src/internationalize/jsonFile/translations.json")

    def test_token(self):
        self.assertEqual(self.data['Token'], "85124f79-0829-4b80-8b5c-d52700d86e46")
    
    def test_translations(self):
        translations = self.data['translations']
        self.assertEqual(len(translations), 2)

        # French
        self.assertEqual(translations[0]['language'], "French")
        self.assertEqual(translations[0]['hello'], "bonjour")
        self.assertEqual(translations[0]['No'], "Non")
        self.assertEqual(translations[0]['Why'], "pourquoi")
    
        # Spanish
        self.assertEqual(translations[1]['language'], "Spanish")
        self.assertEqual(translations[1]['hello'], "Hola")

unittest.main()