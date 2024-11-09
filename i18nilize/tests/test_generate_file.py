from src.internationalize.helpers import generate_file

class TestGenerateFile():                
    def setUp(self):
        token = Token.objects.create()
        self.TEST_TOKEN = str(token.value)
        
        translations_data = {
            'translations': [
                {
                    'language': 'spanish',
                    'hello': 'hola',
                    'thanks': 'gracias'
                }
            ]
        }
        headers = {
            'HTTP_Token': self.TEST_TOKEN
        }

        # create default translations
        response = self.client.post(reverse('process-translations'), translations_data, **headers, format='json')

    def test_generate_file:
        generate_file('spanish', self.TEST_TOKEN)


  

if __name__ == '__main__':
    unittest.main()
