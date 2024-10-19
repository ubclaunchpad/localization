from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Token, Translation
from .utils.translation_utils import *
from .utils.utils import *
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
    def post(self, request, *args, **kwargs):
        """
        Adds new translations to database
        """
        translations_data = request.data
        token_uuid = request.headers.get('Token')

        if not token_uuid:
            return error_response('Token is required.', 400)
        
        if not translations_data:
            return error_response('Translations are required.', 400)
            
        if not is_valid_uuid(token_uuid):
            return error_response('Invalid token.', 400)

        try:
            token = Token.objects.get(value=token_uuid)

            if not validate_translations_data(translations_data):
                return error_response('Translations are improperly formatted.', 400)
            
            new_translations = get_new_translations(translations_data, token)
            if new_translations is False:
                return error_response('Use a PATCH request to make updates to translations.', 400)
            
            success = bulk_create_translations(token, new_translations)
            if not success:
                return error_response('An error occurred while inserting new translations.', 500)

            return success_response({"message": "All translations created successfully."}, 201)
        except Token.DoesNotExist:
            return error_response('Token not found.', 404)