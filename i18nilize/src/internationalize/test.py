import unittest, os
from parser import parse_json_file

# Create your tests here.
class JSONParseTestCase(unittest.TestCase):                
    def setUp(self):
        current_dir = os.path.dirname(__file__)
        self.test_path = os.path.join(current_dir, 'test_json.json')

    def test_parse_json_file(self):
        data = parse_json_file(self.test_path)

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
