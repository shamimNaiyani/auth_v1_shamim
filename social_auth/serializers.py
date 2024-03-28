from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .register import register_social_user
from .google import Google

class GoogleOauthSignInSerializer(serializers.Serializer):
    access_token = serializers.CharField(min_length=6)
    
    
    def validate_access_token(self, access_token):
        user_data = Google.validate(access_token)  
        try:
            user_data['sub'] 
        except:
            raise serializers.ValidationError("Invalid token!") 
        
        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed("Could not verify user.")
        
        user_id = user_data['sub']
        email = user_data['email']
        first_name = user_data['given_name']
        last_name = user_data['family_name']
        provider = 'google'
        
        return register_social_user(provider, email, first_name, last_name)