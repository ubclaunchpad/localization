import unittest, os, json, timeit
from src.internationalize.helpers import get_json, make_translation_map, get_translation

# Create your tests here.
class TestGetJson(unittest.TestCase):                
    def setUp(self):
        current_dir = os.path.dirname(__file__)
        self.test_path = os.path.join(current_dir, 'resources/test_json.json')

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
        self.test_path = os.path.join(current_dir, 'resources/test_invalid_json.json')
        with self.assertRaises(json.JSONDecodeError):
            get_json(self.test_path)

    def test_missing_token(self):
        current_dir = os.path.dirname(__file__)
        self.test_path = os.path.join(current_dir, 'resources/test_no_token.json')
        data = get_json(self.test_path)
        self.assertNotIn('Token', data, "No token")
        self.assertEqual(len(data['translations']), 2)

        french_translation = data['translations'][0]
        self.assertEqual(french_translation['language'], "French")
        self.assertEqual(french_translation['hello'], "bonjour")
        self.assertEqual(french_translation['No'], "Non")
        self.assertEqual(french_translation['Why'], "pourquoi")

        spanish_translation = data['translations'][1]
        self.assertEqual(spanish_translation['language'], "Spanish")
        self.assertEqual(spanish_translation['hello'], "Hola")

    def test_missing_translations(self):
        current_dir = os.path.dirname(__file__)
        self.test_path = os.path.join(current_dir, 'resources/test_no_translations.json')
        data = get_json(self.test_path)
        self.assertEqual(data['Token'], "85124f79-0829-4b80-8b5c-d52700d86e46")
        self.assertNotIn('translations', data, "No translations")

    def test_translation_lookup(self):
        current_dir = os.path.dirname(__file__)
        self.test_path = os.path.join(current_dir, 'resources/test_json.json')
        data = get_json(self.test_path)
        self.translations_map = make_translation_map(data)
        french_translation = get_translation(self.translations_map, 'French')
        print("French Translation: ", french_translation)
        self.assertEqual(french_translation['hello'], 'bonjour')
        self.assertEqual(french_translation['No'], 'Non')
        self.assertEqual(french_translation['Why'], 'pourquoi')

        spanish_translation = get_translation(self.translations_map, 'Spanish')
        print("Spanish Translation: ", spanish_translation)
        self.assertEqual(spanish_translation['hello'], 'Hola')

    def test_translation_lookup_nonexistent(self):
        current_dir = os.path.dirname(__file__)
        self.test_path = os.path.join(current_dir, 'resources/test_json.json')
        data = get_json(self.test_path)
        self.translations_map = make_translation_map(data)
        korean_translation = get_translation(self.translations_map, 'Korean')
        self.assertEqual(korean_translation, "Translation not found")

    def test_translation_lookup_small(self):
        current_dir = os.path.dirname(__file__)
        self.test_path = os.path.join(current_dir, 'resources/test_json.json')
        data = get_json(self.test_path)
        self.translations_map = make_translation_map(data)

        lookup_time = timeit.timeit(
            stmt=lambda:get_translation(self.translations_map, 'French'),
            number=1000
        )

        print("Lookup Time Small File:", lookup_time)
        french_translation = get_translation(self.translations_map, 'French')
        self.assertEqual(french_translation['hello'], 'bonjour')
        self.assertEqual(french_translation['No'], 'Non')
        self.assertEqual(french_translation['Why'], 'pourquoi')

    def test_translation_lookup_big(self):
        current_dir = os.path.dirname(__file__)
        self.test_path = os.path.join(current_dir, 'resources/test_many_json.json')
        data = get_json(self.test_path)
        self.translations_map = make_translation_map(data)

        lookup_time = timeit.timeit(
            stmt=lambda:get_translation(self.translations_map, 'Tagalog'),
            number=1000
        )

        print("Lookup Time Big File:", lookup_time)
        tagalog_translation = get_translation(self.translations_map, 'Tagalog')
        self.assertEqual(tagalog_translation['hello'], 'Kamusta')
        self.assertEqual(tagalog_translation['No'], 'Hindi')
        self.assertEqual(tagalog_translation['Why'], 'Bakit')

if __name__ == '__main__':
    unittest.main()
