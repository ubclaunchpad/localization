# api_helpers.py
from internationalize.helpers import generate_file
from core.i18nilize.services.locale import get_default_language
import globals
from core.i18nilize.views import TokenView
from rest_framework.request import Request
from django.http import HttpRequest


def create_token():
    http_request = HttpRequest()
    http_request.method = 'POST'
    
    request = Request(http_request)

    token_view = TokenView()
    response = token_view.post(request)

    if response.status_code == 201:
        globals.token = response.data.get("value")
        print("Token set.")
    else:
        raise Exception(f"Failed to retrieve token. Status code: {response.status_code}")
    
def generate_default_language_file():
    token = globals.token
    if not token:
        print("Token not found. Creating a new token...")
        create_token()
        token = globals.token
        if not token:
            raise Exception("Failed to create token.")
        
    language = get_default_language()
    if not language:
        raise Exception("Failed to determine the default language.")
    
    generate_file(language, token)
    print(f"Generated translation file for language: {language}")

