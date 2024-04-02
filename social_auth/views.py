from django.shortcuts import render
from rest_framework import status 
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

# custom model 
from .serializers import (
    GoogleOauthSignInSerializer, 
)


class GoogleOauthSignInApiView(GenericAPIView):
    serializer_class = GoogleOauthSignInSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data) 
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['access_token'])
        return Response(data, status=status.HTTP_200_OK)
