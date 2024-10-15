import unittest, os, json
from src.internationalize.helpers import get_json

# Create your tests here.
class JSONParseTestCase(unittest.TestCase):                
    def setUp(self):
        current_dir = os.path.dirname(__file__)
        self.test_path = os.path.join(current_dir, 'test_json.json')

    def test_get_json(self):
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

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            get_json("doesntexist.json")
    
    def test_invalid_json(self):
        current_dir = os.path.dirname(__file__)
        self.test_path = os.path.join(current_dir, 'test_invalid_json.json')
        with self.assertRaises(json.JSONDecodeError):
            get_json(self.test_path)

unittest.main()
