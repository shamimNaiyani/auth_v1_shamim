from django.shortcuts import render
from rest_framework.generics import GenericAPIView

# custom model 
from .serializers import (
    GoogleOauthSignInSerializer, 
)


class GoogleOauthSignInApiView(GenericAPIView):
    serializer_class = GoogleOauthSignInSerializer
    
    

