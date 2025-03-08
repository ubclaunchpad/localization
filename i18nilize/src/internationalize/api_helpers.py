# api_helpers.py

import requests
from . import globals
import sys

def create_token():
    """
    Creates a new token by making a POST request to the central API.
    """
    url = globals.TOKEN_ENDPOINT
    try:
        response = requests.post(url)
        if response.status_code == 201:
            token_value = response.json().get("value")
            globals.token.value = token_value 
            print("Token set.")
        else:
            raise Exception(f"Failed to retrieve token. Status code: {response.status_code}")
    except requests.RequestException as e:
        raise Exception(f"HTTP Request failed: {e}")
    
def create_ms_token():
    """
    Creates a new microservice token by making a POST request to the central API.
    """
    url = globals.MS_TOKEN_ENDPOINT
    try:
        response = requests.post(url)
        if response.status_code == 201:
            token_value = response.json().get("value")
            globals.ms_token.value = token_value 
            print("Microservice Token set.")
        else:
            raise Exception(f"Failed to retrieve token. Status code: {response.status_code}")
    except requests.RequestException as e:
        raise Exception(f"HTTP Request failed: {e}")

def fetch_translation_data(language):
    """
    Fetches translation data for the specified language using the token.
    """
    token = globals.token.value  
    if not token:
        print("Token not found. Creating a new token...")
        create_token()
        token = globals.token.value
        if not token:
            raise Exception("Failed to create token.")
        
    if not language:
        raise Exception("Language parameter is required.")
    
    url = f"{globals.TRANSLATIONS_ENDPOINT}?language={language}" 
    headers = {
        'Authorization': f'Token {token}'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            translations = response.json()
            print(f"Generated translation data for language: {language}")
            return translations
        else:
            print(f"Generated translation data for language: {language}")
            raise Exception(f"No translations found for language: {language}")
    except requests.RequestException as e:
        raise Exception(f"HTTP Request failed: {e}")

# return true if ms_token has writer permissions
# else false
def has_writer_permissions(ms_token):
    try:
        response = requests.post(globals.WRITER_PERMISSIONS_ENDPOINT, headers={'Microservice-Token': ms_token})

        if response.status_code == 200:
            data = response.json()
            editor_token = data.get("editor_token")
            return editor_token == ms_token
        
        elif response.status_code == 404:
            print("project that ms_token is in has not initialized reader/writer permissions yet.")
            return False
        
        else:
            raise Exception(f"Bad HTTP Request: {e}")
        


    except requests.RequestException as e:
        raise Exception(f"HTTP Request failed: {e}")