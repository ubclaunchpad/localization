from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Token, Translation
import uuid
import json

# Create your views here.
class SampleAPIView(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            'message': 'Hey there!'
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        received_data = request.data
        response_data = {
            'message': 'Data received successfully!',
            'received_data': received_data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class TokenView(APIView):
    """
    Endpoint to create a new token or retrieve a token by its ID.
    """

    def post(self, request):
        """
        Create a new token.
        """
        token = Token.objects.create()
        data = {
            'id': token.id,
            'value': str(token.value),
            'created_at': token.created_at.isoformat()
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def get(self, request, value=None):
        """
        Retrieve a token by its value
        """
        if value is None:
            return Response({'error': 'Token value is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = Token.objects.get(value=value)
            data = {
                'id': token.id,
                'value': str(token.value),
                'created_at': token.created_at.isoformat()
            }
            return Response(data, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'error': 'Token not found.'}, status=status.HTTP_404_NOT_FOUND)

class ProcessTranslationsView(APIView):
    """
    Endpoint to add or update translations.
    """

    """
    Test Token
    {
        "id": 5,
        "value": "c84234c3-b507-4ed0-a6eb-8b10116cdef1",
        "created_at": "2024-10-18T03:44:00.547520+00:00"
    }
    """
    
    def post(self, request, *args, **kwargs):
        """
        Adds new translations to database
        """
        translations_data = request.data
        token_id = request.headers.get("Token")

        if not token_id:
            return Response({'error': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not translations_data:
            return Response({'error': 'Translations are required.'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Validate that token_id valid UUID
        try:
            uuid_obj = uuid.UUID(token_id, version=4)
        except ValueError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = Token.objects.get(value=token_id)

            if not self._validate_translations_data(translations_data):
                return Response({'error': 'Invalid translations format.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # TODO: check if all translations are not in DB, if so, add new translations
            # self._add_translations()

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Token.DoesNotExist:
            return Response({'error': 'Token not found.'}, status=status.HTTP_404_NOT_FOUND)

    def _validate_translations_data(self, translations_data):
        """
        Validates translation data structure
        """

        if "translations" not in translations_data:
            return False

        for translations in translations_data["translations"]:
            if "language" not in translations:
                return False

            for key, value in translations.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    return False
        
        return True
    
    def _get_new_translations(self, translations_data, token):
        """
        Returns a set of translations to add to the database. If any translation
        is being updated, returns False (use PATCH endpoint to make updates).
        """
        new_translations = set()
        for translations in translations_data["translations"]:
            language = translations["language"]
            for original_word, translated_word in translations.items():
                if original_word == "language":
                    continue

                try:
                    translation = Translation.objects.get(
                        token=token,
                        original_word=original_word,
                        language=language
                    )

                    # Translation exists and matches, skip
                    if translation.translated_word == translated_word:
                        continue

                    # Translation exists and is being updated; use PATCH endpoint instead.
                    return False

                except Translation.DoesNotExist:
                    new_translations.add((original_word, translated_word, language))
        
        return new_translations