from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class DomainApiView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)


class LinkApiView(APIView):
    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)
