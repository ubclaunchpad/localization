from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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

class PostTranslations(APIView):
    def post(self, request, *args, **kwargs):
        received_data = request.data
        token = request.headers.get("Token")

        response_data = {
            'message': 'Data received successfully!',
            'received_data': received_data,
            'received_token': token
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
