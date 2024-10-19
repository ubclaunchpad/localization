from rest_framework.response import Response
from rest_framework import status
import uuid

ERROR_STATUS_CODE_MAP = {
    500: status.HTTP_500_INTERNAL_SERVER_ERROR,
    400: status.HTTP_400_BAD_REQUEST,
    404: status.HTTP_404_NOT_FOUND,
    403: status.HTTP_403_FORBIDDEN,
}

SUCCESS_STATUS_CODE_MAP = {
    200: status.HTTP_200_OK,
    201: status.HTTP_201_CREATED,
}

def error_response(message, code):
    return Response(
        {'error': message},
        status=ERROR_STATUS_CODE_MAP.get(code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    )

def success_response(data, code):
    return Response(
        data,
        status=SUCCESS_STATUS_CODE_MAP.get(code, status.HTTP_200_OK)
    )

def is_valid_uuid(uuid_to_test, version=4):
    """
    Checks that UUID is valid
    """
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
        return True
    except ValueError:
        return False