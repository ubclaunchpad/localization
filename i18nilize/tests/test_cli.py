import unittest, os, json, timeit
from src.internationalize.helpers import get_json, make_translation_map, get_translation, add_language

# Create your tests here.
class TestCLI(unittest.TestCase):                
    def setUp(self):
        current_dir = os.path.dirname(__file__)
        self.test_path = os.path.join(current_dir, 'resources/test_json.json')

    def test_add_language(self):
        data = get_json(self.test_path)

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

        self = add_language("Korean")
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

        spanish_translation = data['translations'][2]
        self.assertEqual(spanish_translation['language'], "Korean")

if __name__ == '__main__':
    unittest.main()
