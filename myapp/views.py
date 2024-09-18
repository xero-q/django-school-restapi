from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class HomeView(APIView):
    def get(self, request):
        name = request.query_params['name']
        return Response('Hola Mundo, ' + name,status=status.HTTP_200_OK)
