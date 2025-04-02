# api_helpers.py

import requests
from . import globals
from dotenv import load_dotenv
import os
from .helpers import (
    write_env_var
)

ENV_FILE_PATH = globals.ENV_FILE

def create_token():
    """
    Creates a new token by making a POST request to the central API.
    stores the token in the .env file.
    """
    url = globals.TOKEN_ENDPOINT
    try:
        response = requests.post(url)
        if response.status_code == 201:
            token_value = response.json().get("value")

            # Write it to .env
            write_env_var("GROUP_TOKEN", token_value)

            # Write it to globals
            globals.token.value = token_value

            print("Group Token set and saved to .env.")
        else:
            raise Exception(f"Failed to retrieve token. Status code: {response.status_code}")
    except requests.RequestException as e:
        raise Exception(f"HTTP Request failed: {e}")
    

def assign_token(token):
    """
    Update a group token in .env and in the server.
    """
    # Save it to .env and globals
    globals.token = token
    write_env_var("GROUP_TOKEN", token)

    load_dotenv(ENV_FILE_PATH)
    ms_token = os.getenv("MS_TOKEN")

    if not ms_token:
        raise Exception("MS_TOKEN is not set in .env")

    # PATCH URL now targets the existing microservice token
    url = f"{globals.MS_TOKEN_ENDPOINT}{ms_token}/"

    # We want to change the project_token to this new group token
    payload = {
        "project_token": token
    }

    try:
        response = requests.patch(url, json=payload)

        if response.status_code == 200:
            print("Group token successfully updated to:", token)

            # Optionally confirm the updated MS token still matches
            globals.ms_token.value = ms_token
        else:
            raise Exception(f"Failed to update group token. Status code: {response.status_code}, Response: {response.text}")
    except requests.RequestException as e:
        raise Exception(f"HTTP Request failed: {e}")
    

def create_ms_token():
    """
    Creates a new microservice token by making a POST request to the central API.
    Stores the token in the .env file.
    """
    load_dotenv(ENV_FILE_PATH)
    group_token = os.getenv("GROUP_TOKEN")

    if not group_token:
        raise Exception("GROUP_TOKEN is not set in .env")

    url = f"{globals.MS_TOKEN_ENDPOINT}{group_token}/"

    try:
        response = requests.post(url)
        if response.status_code == 201:
            token_value = response.json().get("value")

            # Write it to .env
            write_env_var("MS_TOKEN", token_value)

            # Write it to globals
            globals.ms_token.value = token_value

            print("Microservice Token set and saved to .env.")
        else:
            raise Exception(f"Failed to retrieve token. Status code: {response.status_code}")
    except requests.RequestException as e:
        raise Exception(f"HTTP Request failed: {e}")

def fetch_translation_data(language):
    """
    Fetches translation data for the specified language using the token.
    """

    load_dotenv(ENV_FILE_PATH)
    token = os.getenv("GROUP_TOKEN")

    if not token:
        print("Token not found. Creating a new token...")
        create_token()
        load_dotenv(ENV_FILE_PATH)
        token = os.getenv("GROUP_TOKEN")

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
        response = requests.get(globals.WRITER_PERMISSIONS_ENDPOINT, headers={'Microservice-Token': ms_token})

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

    load_dotenv(ENV_FILE_PATH)
    ms_token = os.getenv("MS_TOKEN")

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

    load_dotenv(ENV_FILE_PATH)
    ms_token = os.getenv("MS_TOKEN")
    
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
            print("Microservice token not found.")
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

