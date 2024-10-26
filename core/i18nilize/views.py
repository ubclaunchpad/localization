# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Token, Translation
from i18nilize.utils import is_valid_uuid
from i18nilize.services import translation_processor as tp


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

    def post(self, request):
        """
        Adds new translations to database
        """
        translations_data = request.data
        token_uuid = request.headers.get('Token')

        if not token_uuid:
            return Response({'error': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not is_valid_uuid(token_uuid):
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        if not translations_data:
            return Response({'error': 'Translations data is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = Token.objects.get(value=token_uuid)

            if not tp.validate_translations_data(translations_data):
                return Response(
                    {'error': 'Translations are improperly formatted.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            new_translations = tp.get_new_translations(translations_data, token)
            if new_translations is False:
                return Response(
                    {'error': 'Use a PATCH request to make updates to translations.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            success, added_count = tp.bulk_create_translations(token, new_translations)
            if not success:
                return Response(
                    {'error': 'An error occurred while inserting new translations.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            if added_count == 0:
                return Response(
                    {'message': 'All translations created successfully.', 'added_count': added_count},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': 'All translations created successfully.', 'added_count': added_count},
                    status=status.HTTP_201_CREATED
                )

        except Token.DoesNotExist:
            return Response({'error': 'Token not found.'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        """
        Update existing translations in the database. Fails if new translations are being added.
        """
        translations_data = request.data
        token_uuid = request.headers.get('Token')

        if not token_uuid:
            return Response({'error': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not is_valid_uuid(token_uuid):
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        if not translations_data:
            return Response({'error': 'Translations data is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # extract languages, key to values from translations_data
        try:
            token = Token.objects.get(value=token_uuid)

            if not tp.validate_translations_data(translations_data):
                return Response(
                    {'error': 'Translations are improperly formatted.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            updated_translations = tp.get_updated_translations(translations_data, token)
            if updated_translations is False:
                return Response(
                    {'error': 'Use a POST request to make new translations.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            success, updated_count = tp.bulk_update_translations(token, updated_translations)
            if not success:
                return Response(
                    {'error': 'An error occurred while updating translations.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            if updated_count == 0:
                return Response(
                    {'message': 'All translations updated successfully.', 'updated_count': updated_count},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': 'All translations updated successfully.', 'updated_count': updated_count},
                    status=status.HTTP_201_CREATED
                )

        except Token.DoesNotExist:
            return Response({'error': 'Token not found.'}, status=status.HTTP_404_NOT_FOUND)

class TranslationView(APIView):
    """
    CRUD endpoint to read single translation
    """

    def post(self, request):
        """
        Create a new single translation.
        """

        # get token if it exists
        token_value = request.headers.get('Token')
        try:
            token = Token.objects.get(value=token_value)
        except Token.DoesNotExist:
            return Response({'error': 'Token not found.'}, status=status.HTTP_404_NOT_FOUND)

        # get translation from api body
        if len(request.query_params) > 2:
                return Response({"error": "query params should only include language and one translation pair"}, status=status.HTTP_400_BAD_REQUEST)
        language = request.query_params.get('language')
        translation_pair = {key: value for key, value in request.query_params.items() if key != "language"}        

        # Check for missing parameters
        if not language or len(translation_pair.items()) != 1:
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)
        
        original_word, translated_word = list(translation_pair.items())[0]

        # Check if translation already exists
        try:
            # Try to retrieve an existing translation
            existing_translation = Translation.objects.get(token=token, original_word=original_word, language=language)

            # Check if the existing translated word matches with the new one
            if existing_translation.translated_word != translated_word:
                return Response({"error": "Existing translation doesn't match new translation!"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Existing translation already exists!"}, status=status.HTTP_200_OK)

        # Create the translation if it doesn't already exist
        except Translation.DoesNotExist:
            translation = Translation.objects.create(token=token, original_word=original_word, translated_word=translated_word, language=language)
            data = {
                "message": "translation successfuly created!",
                "language": translation.language,
                "original_word": translation.original_word,
                "translated_word": translation.translated_word
            }
            return Response(data, status=status.HTTP_201_CREATED)

    def get(self, request, value=None):
        """
        Retrieve a translation by its original word and token
        """
       # get token if it exists
        token_value = request.headers.get('Token')
        try:
            token = Token.objects.get(value=token_value)
        except Token.DoesNotExist:
            return Response({'error': 'Token not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # get word and language to translate to from api body
        original_word = request.query_params.get('original_word')
        language = request.query_params.get('language')

        # Check for missing parameters
        if not original_word or not language:
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        # return translation if it exists
        try:
            translation = Translation.objects.get(token=token, original_word=original_word, language=language)
            data = {
                "language": translation.language,
                "original_word": translation.original_word,
                "translated_word": translation.translated_word
            }
            return Response(data, status=status.HTTP_200_OK)
        
        except Translation.DoesNotExist:
            return Response({"error": "Translation not found for given language and word!"}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request):
        """
        Update a new single translation.
        """

        # get token if it exists
        token_value = request.headers.get('Token')
        try:
            token = Token.objects.get(value=token_value)
        except Token.DoesNotExist:
            return Response({'error': 'Token not found.'}, status=status.HTTP_404_NOT_FOUND)

        # get translation from api body
        if len(request.query_params) > 2:
                return Response({"error": "query params should only include language and one translation pair"}, status=status.HTTP_400_BAD_REQUEST)
        language = request.query_params.get('language')
        translation_pair = {key: value for key, value in request.query_params.items() if key != "language"}        

        # Check for missing parameters
        if not language or len(translation_pair.items()) != 1:
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)
        
        original_word, translated_word = list(translation_pair.items())[0]

        # Check if translation already exists
        try:
            # Try to retrieve an existing translation
            existing_translation = Translation.objects.get(token=token, original_word=original_word, language=language)

            # Check if the existing translated word matches with the new one
            if existing_translation.translated_word != translated_word:
                old_translated_word = existing_translation.translated_word
                existing_translation.translated_word = translated_word
                existing_translation.save()
                data = {
                    "message": "Translation updated successfuly!",
                    "language": existing_translation.language,
                    "original_word": existing_translation.original_word,
                    "original_translated_word": old_translated_word,
                    "updated_translated_word": existing_translation.translated_word
                }
                return Response(data, status=status.HTTP_200_OK)

            # otherwise, existing translation is the same as the new translation
            return Response({"message": "Existing translation already exists!"}, status=status.HTTP_200_OK)

        # Create the translation if it doesn't already exist
        except Translation.DoesNotExist:
            translation = Translation.objects.create(token=token, original_word=original_word, translated_word=translated_word, language=language)
            data = {
                "message": "Translation created successfuly!",
                "language": translation.language,
                "original_word": translation.original_word,
                "translated_word": translation.translated_word
            }
            return Response(data, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        """
        Delete a new single translation.
        """

        # get token if it exists
        token_value = request.headers.get('Token')
        try:
            token = Token.objects.get(value=token_value)
        except Token.DoesNotExist:
            return Response({'error': 'Token not found.'}, status=status.HTTP_404_NOT_FOUND)

        # get translation from api body
        if len(request.query_params) > 2:
                return Response({"error": "query params should only include language and one translation pair"}, status=status.HTTP_400_BAD_REQUEST)
        language = request.query_params.get('language')
        translation_pair = {key: value for key, value in request.query_params.items() if key != "language"}        

        # Check for missing parameters
        if not language or len(translation_pair.items()) != 1:
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)
        
        original_word, translated_word = list(translation_pair.items())[0]

        # Check if translation exists
        try:
            translation = Translation.objects.get(token=token, original_word=original_word, translated_word=translated_word, language=language)
            translation.delete()
            data = {
                "message": "Translation deleted successfuly!",
                "language": translation.language,
                "original_word": translation.original_word,
                "translated_word": translation.translated_word
            }
            return Response(data, status=status.HTTP_200_OK)

        # Throw a bad request if the translation doesn't exist
        except Translation.DoesNotExist:
            return Response({"error": "translation doesn't exist!"}, status=status.HTTP_400_BAD_REQUEST)