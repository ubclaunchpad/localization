from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Token
import uuid

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
    
    # Check if token exists: import model
    # Check if all translations are present in database, if not, add new translation
        # If translation already exists and translation does match, return status code 400
    # Return 201 status code
    def post(self, request, *args, **kwargs):
        """
        Adds new translations to database
        """
        try:
            received_data = request.data
            token_id = request.headers.get("Token")
            token = Token.objects.get(value=token_id)

            response_data = {
                'message': 'Data received successfully!',
                'received_data': received_data,
                'received_token': token
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Token.DoesNotExist:
            return Response({'error': 'Token not found.'}, status=status.HTTP_404_NOT_FOUND)