from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Token, Translation
from .services.translation_processor import *
from .utils import *
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

            if not validate_translations_data(translations_data):
                return Response(
                    {'error': 'Translations are improperly formatted.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            new_translations = get_new_translations(translations_data, token)
            if new_translations is False:
                return Response(
                    {'error': 'Use a PATCH request to make updates to translations.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            success, added_count = bulk_create_translations(token, new_translations)
            if not success:
                return Response(
                    {'error': 'An error occurred while inserting new translations.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            if added_count == 0:
                return Response(
                    {'message': 'No new translations to add.', 'added_count': added_count},
                    status=status.HTTP_200_OK
                )

            return Response(
                {'message': 'All translations created successfully.', 'added_count': added_count},
                status=status.HTTP_201_CREATED
            )
        except Token.DoesNotExist:
            return Response({'error': 'Token not found.'}, status=status.HTTP_404_NOT_FOUND)