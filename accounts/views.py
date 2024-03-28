# from threading import Thread
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserRegisterSerializer, 
    UserLoginSerializer, 
    UserLogoutSerializer,
    PasswordResetRequestSerializer,
    SetNewPasswordSerializer,
)
from .utils import send_otp_to_new_registered_user
from .models import OTP, User


class UserRegisterView(GenericAPIView):
    serializer_class = UserRegisterSerializer
    
    def post(self, request):
        # get post the data from request  
        user_data = request.data
        # serialize user_data. serialization means convert the data type into native python data type
        serializer = self.serializer_class(data=user_data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data 
            # since user data is valid and registered in the database so send OTP to the 
            # user email for email verification 
            send_otp_to_new_registered_user(request=request, email=user.get("email"))
            # do the email sending in the separate thread 
            # thread = Thread(target=send_otp_to_new_registered_user, args=(request, user.get("email")))
            # thread.start()

            
            return Response({
                "data": user,
                "message": f"Hi {user.get('first_name')}! Thanks for signing up! We send OTP. Plese check your email for varification!"
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyUserEmailView(GenericAPIView):
    def post(self, request):
        otp = request.data.get('otp')
        
        try:
            user_code_obj = OTP.objects.get(code=otp)
            user = user_code_obj.user 
            if not user.is_verified:
                user.is_verified = True 
                user.save() 
                return Response({
                    "message": "Email verification done successfully!"
                }, status=status.HTTP_200_OK)
            
            return Response({
                "message": "User already verified!"
            }, status=status.HTTP_204_NO_CONTENT)
                
        except OTP.DoesNotExist:
            return Response({
                'message': 'Invalid OTP'
            }, status=status.HTTP_404_NOT_FOUND)


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        user_data = request.data 
        serializer = self.serializer_class(data=user_data, context={"request": request})
        
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class UserLogoutApiView(GenericAPIView):
    # for logout user should be authenticated 
    serializer_class = UserLogoutSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user_data = request.data 
        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Logout successfully!"}, status=status.HTTP_204_NO_CONTENT)


class PasswordResetRequestApiView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    
    def post(self, request):
        user_data = request.data 
        serializer = self.serializer_class(data=user_data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({
                "message": "Please check your email for password reset link!"
            }, status=status.HTTP_205_RESET_CONTENT)


class PasswordResetConfirmApiView(GenericAPIView):
    # http://localhost:8000/api/v1/auth/password-reset-confirm/OQ/c2tfcv-6f15041026a97ab1c12f6e647bc844d6/
    def get(self, request, uidb64, token):
        # In this url uidb64 = OQ and token = c2tfcv-6f15041026a97ab1c12f6e647bc844d6
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64)) 
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user=user, token=token):
                return Response({"message": "Invalid link or used!"}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                    "success": True, 
                    "message": "Credentials is valid!",
                    "uidb64": uidb64,
                    "token": token
                }, status=status.HTTP_205_RESET_CONTENT)
        except DjangoUnicodeDecodeError:
            return Response({"message": "Unauthorized attempt!"}, status=status.HTTP_401_UNAUTHORIZED) 


class SetNewPasswordApiView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer 
    
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
                "message": "Password reset successful! Please check your email!"
            }, status=status.HTTP_200_OK)
    

class UserProfile(GenericAPIView):
    '''from rest_framework.permissions import IsAuthenticated'''
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        data = {
            "Developed by": "SHAMIM, Software Engineer Intern, Naiyani", 
            "msg": "The authentication system is working perfectly!" 
        }
        
        return Response(data, status=status.HTTP_200_OK)