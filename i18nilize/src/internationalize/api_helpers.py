# api_helpers.py

import requests
from . import globals  
import sys

def create_token():
    """
    Creates a new token by making a POST request to the central API.
    """
    url = "http://localhost:8000/api/token/" 
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
    
    url = f"http://localhost:8000/api/translations/?language={language}" 
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
