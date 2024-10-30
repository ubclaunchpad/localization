import uuid
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .models import Token

def is_valid_uuid(uuid_string, version=4):
    """
    Checks that a string is a valid UUID
    """
    try:
        uuid.UUID(uuid_string, version=version)
        return True
    except ValueError:
        return False

def require_valid_token(func):
    """
    Validates Token, wraps around CRUD methods in views.py
    """
    @wraps(func)
    def wrapper(self, request):
        token_value = request.headers.get('Token')
        if not token_value:
            return Response({'error': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not is_valid_uuid(token_value):
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = Token.objects.get(value=token_value)
            request.token = token
        except Token.DoesNotExist:
            return Response({'error': 'Missing valid token.'}, status=status.HTTP_404_NOT_FOUND)

        return func(self, request)

    return wrapper