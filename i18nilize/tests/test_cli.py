import unittest, os, json, timeit
from src.internationalize.helpers import get_json, make_translation_map, get_translation, add_language

# Create your tests here.
class TestCLI(unittest.TestCase):                
# To test:
# In i18nilize directory, run
# python -m tests.test_cli

# UNTIL THE REFACTORING IS COMPLETED TO MAP INDIVIDUAL LANGUAGES TO FILE, TEST MUST BE MANUALLY COMPLETED BY REMOVING THE KOREAN
# LANGUAGE EVERY TIME YOU RUN THE TEST IN LANGUAGES.json
    def test_add_language(self):
        data = get_json('src/internationalize/resources/languages.json')

        print("Checking Number of Translations:")
        self.assertEqual(data['Token'], "85124f79-0829-4b80-8b5c-d52700d86e46")
        self.assertEqual(len(data['translations']), 2)

        print("Checking French Translations:")
        french_translation = data['translations'][0]
        self.assertEqual(french_translation['language'], "French")
        self.assertEqual(french_translation['hello'], "bonjour")
        self.assertEqual(french_translation['No'], "Non")
        self.assertEqual(french_translation['Why'], "pourquoi")

        print("Checking Spanish Translations:")
        spanish_translation = data['translations'][1]
        self.assertEqual(spanish_translation['language'], "Spanish")
        self.assertEqual(spanish_translation['hello'], "Hola")

        add_language("Korean")
        data = get_json('src/internationalize/resources/languages.json')
        self.assertEqual(data['Token'], "85124f79-0829-4b80-8b5c-d52700d86e46")
        self.assertEqual(len(data['translations']), 3)

        french_translation = data['translations'][0]
        self.assertEqual(french_translation['language'], "French")
        self.assertEqual(french_translation['hello'], "bonjour")
        self.assertEqual(french_translation['No'], "Non")
        self.assertEqual(french_translation['Why'], "pourquoi")

        spanish_translation = data['translations'][1]
        self.assertEqual(spanish_translation['language'], "Spanish")
        self.assertEqual(spanish_translation['hello'], "Hola")

        korean_translation = data['translations'][2]
        self.assertEqual(korean_translation['language'], "Korean")
        print("Test passed!")

    def test_add_existing_language(self):
        data = get_json('src/internationalize/resources/languages.json')

        self.assertEqual(data['Token'], "85124f79-0829-4b80-8b5c-d52700d86e46")
        self.assertEqual(len(data['translations']), 2)

        french_translation = data['translations'][0]
        self.assertEqual(french_translation['language'], "French")
        self.assertEqual(french_translation['hello'], "bonjour")
        self.assertEqual(french_translation['No'], "Non")
        self.assertEqual(french_translation['Why'], "pourquoi")

        spanish_translation = data['translations'][1]
        self.assertEqual(spanish_translation['language'], "Spanish")
        self.assertEqual(spanish_translation['hello'], "Hola")

        add_language("Spanish")
        self.assertEqual(data['Token'], "85124f79-0829-4b80-8b5c-d52700d86e46")
        self.assertEqual(len(data['translations']), 2)

        french_translation = data['translations'][0]
        self.assertEqual(french_translation['language'], "French")
        self.assertEqual(french_translation['hello'], "bonjour")
        self.assertEqual(french_translation['No'], "Non")
        self.assertEqual(french_translation['Why'], "pourquoi")

        spanish_translation = data['translations'][1]
        self.assertEqual(spanish_translation['language'], "Spanish")
        self.assertEqual(spanish_translation['hello'], "Hola")

if __name__ == '__main__':
    unittest.main()
