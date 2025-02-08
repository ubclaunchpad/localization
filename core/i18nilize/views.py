# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MicroserviceToken, Token, Translation, Writer
from i18nilize.utils import is_valid_uuid
from i18nilize.utils import require_valid_token
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

class TestTokenView(APIView):
    """
    Endpoint to delete all translations tied to a token for testing.
    """
    @require_valid_token
    def delete(self, request):
        token = request.token
        try:
            translations = Translation.objects.filter(token=token)
            for t in translations:
                t.delete()
        except Exception as e:
            print(e)
            return Response({'error': 'Could not delete all translations for given token.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message': 'Deleted all translations tied to given token.'}, status=status.HTTP_200_OK)

class ProcessTranslationsView(APIView):
    """
    Endpoint to add or update translations.
    """

    @require_valid_token
    def post(self, request):
        """
        Adds new translations to database
        """
        token = request.token

        translations_data = request.data
        if not translations_data:
            return Response({'error': 'Translations data is required.'}, status=status.HTTP_400_BAD_REQUEST)

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

    @require_valid_token
    def patch(self, request):
        """
        Update existing translations in the database. Fails if new translations are being added.
        """
        token = request.token

        translations_data = request.data
        if not translations_data:
            return Response({'error': 'Translations data is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # extract languages, key to values from translations_data
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

    @require_valid_token
    def get(self, request):
        """
        Fetch translations for a given language.
        """
        token = request.token
        language = request.query_params.get('language')

        translations = tp.get_translations_by_language(language, token)
        if not translations:
            return Response(
                {'error': f'No translations found for {language}.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(translations, status=status.HTTP_200_OK)

class TranslationView(APIView):
    """
    CRUD endpoint to read single translation
    """

    def get_translation_data(self, request):
        if len(request.query_params) > 2:
                return None, None, None, Response({"error": "query params should only include language and one translation pair!"}, status=status.HTTP_400_BAD_REQUEST)
        language = request.query_params.get('language')
        translation_pair = {key: value for key, value in request.query_params.items() if key != "language"}        

        # validate query parameters
        if not language or len(translation_pair.items()) < 1:
            return None, None, None, Response({"error": "Missing required fields in query params."}, status=status.HTTP_400_BAD_REQUEST)
        
        original_word, translated_word = list(translation_pair.items())[0]
        if original_word.isdigit() or translated_word.isdigit():
            return None, None, None, Response({"error": "Translation pair must be in string format!"}, status=status.HTTP_400_BAD_REQUEST)

        return language, original_word, translated_word, None

    @require_valid_token
    def post(self, request):
        """
        Create a new single translation.
        """
        token = request.token

        # get translation from api body
        language, original_word, translated_word, error_response = self.get_translation_data(request)

        # return error response if there was an error retreiving translation data
        if error_response:
            return error_response
        
        # Check if translation already exists
        try:
            # Try to retrieve an existing translation
            existing_translation = Translation.objects.get(token=token, original_word=original_word, language=language)

            # Check if the existing translated word matches with the new one
            if existing_translation.translated_word != translated_word:
                return Response({"error": "Use a PATCH request to make updates to translations."}, status=status.HTTP_400_BAD_REQUEST)

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

    @require_valid_token
    def get(self, request):
        """
        Retrieve a translation by its original word and token
        """
        token = request.token
        
        # get word and language to translate to from api body
        original_word = request.query_params.get('original_word')
        language = request.query_params.get('language')

        # Check for missing parameters
        if not original_word or not language:
            return Response({"error": "Missing required fields in query params."}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({"error": "Translation not found for given language and word!"}, status=status.HTTP_404_NOT_FOUND)
        
    @require_valid_token
    def patch(self, request):
        """
        Update a new single translation.
        """
        token = request.token

        # get translation from api body
        language, original_word, translated_word, error_response = self.get_translation_data(request)

        # return error response if there was an error retreiving translation data
        if error_response:
            return error_response

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
                return Response(data, status=status.HTTP_201_CREATED)

            # otherwise, existing translation is the same as the new translation
            return Response({"message": "Existing translation already exists!"}, status=status.HTTP_200_OK)

        # Create the translation if it doesn't already exist
        except Translation.DoesNotExist:
            return Response({'error': 'Use a POST request to make new translations.'}, status=status.HTTP_400_BAD_REQUEST)
    
    @require_valid_token
    def delete(self, request):
        """
        Delete a new single translation.
        """
        token = request.token

        # get translation from api body
        language, original_word, translated_word, error_response = self.get_translation_data(request)

        # return error response if there was an error retreiving translation data
        if error_response:
            return error_response

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
            return Response({"error": "translation doesn't exist!"}, status=status.HTTP_404_NOT_FOUND)

class PullTranslations(APIView):
    """
    Pulls all translations for a given token.
    """
    @require_valid_token
    def get(self, request):
        token = request.token

        try:
            translations = Translation.objects.filter(token=token)

            # Consolidate all translations into single dictionary following
            # the format of local translation files to overwrite files easily.
            response_data = {}
            for translation in translations:
                language = translation.language.lower()
                original_word = translation.original_word
                translated_word = translation.translated_word

                if language not in response_data:
                    response_data[language] = {}
                response_data[language][original_word] = translated_word
        except Exception as e:
            print(e)
            return Response({"error": "could not fetch translations"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(response_data, status=status.HTTP_200_OK)
    
class WriterPermissionView(APIView):
    """
    API endpoint to manage writer permissions to a microservice.
    
    The microservice must include its unique microservice token either in the
    'Microservice-Token' header or in the request body under 'microservice_token'.
    
    The view looks up the MicroserviceToken instance, gets its associated project token,
    and then creates, updates, or deletes a Writer record so that the microservice can manage their writer permissions.
    """

    def post(self, request):
        # obtain the microservice token from headers or request data
        microservice_token_value = (
            request.headers.get("Microservice-Token") or 
            request.data.get("microservice_token")
        )
        if not microservice_token_value:
            return Response(
                {"error": "Microservice token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not is_valid_uuid(microservice_token_value):
            return Response(
                {"error": "Invalid microservice token."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # get the MicroserviceToken instance
        try:
            microservice_token = MicroserviceToken.objects.get(
                microservice_token=microservice_token_value
            )
        except MicroserviceToken.DoesNotExist:
            return Response(
                {"error": "Microservice token not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        project_token = microservice_token.project_token

        # check if a Writer record already exists for this project
        writer_permission = Writer.objects.filter(project_token=project_token).first()
        if writer_permission:
            # if the current microservice is already the writer, no change is needed
            if writer_permission.editor_token == microservice_token:
                return Response(
                    {"message": "Microservice already has writer permissions."},
                    status=status.HTTP_200_OK
                )
            else:
                # another microservice already holds writer permissions
                return Response(
                    {"error": "Writer permissions already granted to another microservice."},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            # no writer exists for this project yet, grant writer permissions
            writer_permission = Writer.objects.create(
                project_token=project_token,
                editor_token=microservice_token
            )
            return Response(
                {"message": "Writer permissions granted."},
                status=status.HTTP_201_CREATED
            )


    def delete(self, request):
        # obtain the microservice token from headers or request data
        microservice_token_value = (
            request.headers.get("Microservice-Token") or 
            request.data.get("microservice_token")
        )
        if not microservice_token_value:
            return Response(
                {"error": "Microservice token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not is_valid_uuid(microservice_token_value):
            return Response(
                {"error": "Invalid microservice token."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # get the MicroserviceToken instance
        try:
            microservice_token = MicroserviceToken.objects.get(
                microservice_token=microservice_token_value
            )
        except MicroserviceToken.DoesNotExist:
            return Response(
                {"error": "Microservice token not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        project_token = microservice_token.project_token

        # check if a Writer record exists for this project
        writer_permission = Writer.objects.filter(project_token=project_token).first()
        if writer_permission:
            # if the current microservice is the writer, remove successfuly
            if writer_permission.editor_token == microservice_token:
                writer_permission = Writer.objects.get(
                    project_token=project_token,
                    editor_token=microservice_token
                )
                writer_permission.delete()
                data = {
                    "message": "Writer permissions removed successfuly!",
                    "project": project_token
                }
                return Response(
                    data,
                    status=status.HTTP_200_OK
                )
            else:
                # another microservice already holds writer permissions
                return Response(
                    {"error": "Remove failed, current microservice has no writer permissions."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # no writer exists for this project yet, cannot remove
            return Response(
                {"error": "Remove failed, no existing editor token found for project"},
                status=status.HTTP_404_NOT_FOUND)