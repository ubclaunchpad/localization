# to be removed

from src.internationalize.helpers import generate_file
from core.i18nilize.models import Token
import requests

def integration_test():
    # create token
    token_response = requests.post('http://localhost:8000/api/create-token/')
    token_data = token_response.json()
    token = token_data['value']

    # create translations
    translations_data = {
        'translations': [
            {
                'language': 'french',
                'hello': 'bonjour',
                'thanks': 'merci'
            }
        ]
    }  
    headers = {
        'Authorization': f'Token {token}'
    }
    translations_response = requests.post(
        'http://localhost:8000/api/process-translations/',
        data=translations_data,
        headers=headers
    )

    generate_file('french', token)
    
integration_test()