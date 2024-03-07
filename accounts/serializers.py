from django.contrib.auth import authenticate
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site 
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import User
from .utils import send_reset_password_link_to_email, send_new_password_to_email


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=64, write_only=True)
    password2 = serializers.CharField(min_length=8, max_length=64, write_only=True)
    
    class Meta:
        model = User  
        fields = ["email", "first_name", "last_name", "password", "password2"]
        
    def validate(self, attrs):
        password = attrs.get("password", "")
        password2 = attrs.get("password2", "")
        
        if password != password2:
            raise serializers.ValidationError("Password does not match!")
        
        return attrs 
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get("email"),
            password=validated_data.get("password"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name")
        )
        
        return user 


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=155, min_length=6)
    password=serializers.CharField(max_length=68, write_only=True)
    full_name=serializers.CharField(max_length=255, read_only=True)
    access_token=serializers.CharField(max_length=255, read_only=True)
    refresh_token=serializers.CharField(max_length=255, read_only=True)
    
    
    class Meta:
        model = User 
        fields = ["email", "password", "full_name", "access_token", "refresh_token"] 
    
    
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        request = self.context.get("request")
        
        user = authenticate(request, email=email, password=password)
        
        if not user:
            raise AuthenticationFailed("UnAuthorized access!") 

        if not user.is_verified:
            raise AuthenticationFailed("Please verify your account with OTP. You got the email with OTP after registration! \n Check your email inbox or spam!")

        # program reach this line means there is a valid user with this email and password and this email account is verified 
        
        # 1. we have to give the user access and refresh token 
        user_token = user.get_user_refresh_and_access_token
        
        return {
            "email": user.email,
            "full_name": user.get_user_fullname,
            "access_token": user_token.get("access"),
            "refresh_token": user_token.get("refresh"),
        }
        

class UserLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    
    default_error_messages = {
        'bad_token': ('Token is expired!')
    }
    
    def validate(self, attrs):
        self.token = attrs.get("refresh_token")
        return attrs
    
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist() 
        except TokenError:
            return self.fail('bad_token') 
    

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=10, max_length=255)
    
    class Meta:
        fields = ["email"]
    
    def validate(self, attrs):
        email = attrs.get("email")
        user = User.objects.get(email=email)
        
        if user:
            # convert userId to base 64 user id using urlsafe_base64_encode
            # from django.utils.http 
            uidb64 = urlsafe_base64_encode(force_bytes(user.id)) 
            token = PasswordResetTokenGenerator().make_token(user)
            current_site_domain = get_current_site(request=self.context.get("request")).domain
            relative_link = reverse(viewname="password-reset-confirm", kwargs={'uidb64': uidb64, 'token': token})
            abslink = f"http://{current_site_domain}{relative_link}"
            
            email_body = f"Hi {user.get_user_fullname}! \nPlease use this one time link for password reset!\n Password reset link: {abslink}"
            
            email_data = {
                'to_email': user.email,
                'subject': f"Password Reset Link from {current_site_domain}",
                'body': email_body,
            }
            
            send_reset_password_link_to_email(email_data)
            
        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=64)
    confirm_password = serializers.CharField(min_length=8, max_length=64)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    
    class Meta:
        fields = ["password", "confirm_password", "uidb64", "token"]
    
    def validate(self, attrs):
        try:
            password = attrs.get("password")
            confirm_password = attrs.get("confirm_password")
            uidb64 = attrs.get("uidb64")
            token = attrs.get("token")
            
            user_id = force_str(urlsafe_base64_decode(uidb64)) 
            user = User.objects.get(id=user_id)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("Invalid reset link!", 401)
            
            if password != confirm_password:
                raise AuthenticationFailed("Passwords does not match!", 401) 
            
            # sometimes user generate password. so it is hard to memorize 
            # for better user experience we can send new email with 
            # new password 
            
            data = {
                "subject": "New password!", 
                "body": f"Hay {user.first_name}! \n Here is your new password {password}\nplease don't shear this email!",
                "to": user.email
            }
            
            user.set_password(password)
            user.save()
            
            send_new_password_to_email(data)
            
            return user 
            
            
        except Exception as e:
            raise AuthenticationFailed("Invalid link!", 401) 