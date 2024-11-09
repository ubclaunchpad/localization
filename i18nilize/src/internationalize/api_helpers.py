# token_manager.py
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
