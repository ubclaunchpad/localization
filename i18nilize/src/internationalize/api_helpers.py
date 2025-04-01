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
    
def relinquish_writer_permissions():
    """
    Relinquishes writer permissions for the current microservice token.
    """
    ms_token = globals.ms_token.value
    if not ms_token:
        print("Microservice token not found. No permissions to relinquish.")
        return False
    
    try:
        response = requests.delete(
            globals.WRITER_PERMISSIONS_ENDPOINT, 
            headers={'Microservice-Token': ms_token}
        )
        
        if response.status_code == 200:
            print("Writer permissions relinquished successfully.")
            return True
        elif response.status_code == 404:
            print("Error: No writer permissions found for this project.")
            return False
        elif response.status_code == 400:
            print("Error: Current microservice does not have writer permissions.")
            return False
        else:
            print(f"Error: Failed to relinquish writer permissions. Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return False
    
def request_writer_permissions():
    """
    Requests permissions to modify shared translations
    """
    ms_token = globals.ms_token.value
    if not ms_token:
        print("Error: Microservice Token is null.")
        return False
    
    try:
        response = requests.post(
            globals.WRITER_PERMISSIONS_ENDPOINT, 
            headers={"Microservice-Token": ms_token}
        )

        if response.status_code == 200 or response.status_code == 201:
            print("Writer permission granted.")
            return True
        elif response.status_code == 400:
            print("No valid microservice token.")
            return False
        elif response.status_code == 404:
            print("WMicroservice token not found.")
            return False
        elif response.status_code == 403:
            print("Writer permissions already granted to another microservice.")
            return False
        else:
            print(f"Error: Failed to request writer permissions. Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return False

