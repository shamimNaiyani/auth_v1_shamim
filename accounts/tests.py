from .models import User, OTP
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status 

class AccountsAppTestCases(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.data = {
            "email": "shamim@gmail.com",
            "first_name": "Software",
            "last_name": "Engineer",
            "password": "test1234",
            "password2": "test1234"
        }   
        self.url = "/api/v1/auth/register/"
    
    def test_userRegistrationApiView_with_all_necessary_valid_info(self):
        """test RegisterGenericApiView with all necessary info"""
        data = self.data 
        response = self.client.post(self.url, data) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().first_name, "Software")
        self.assertEqual(User.objects.get().last_name, "Engineer")
        self.assertEqual(User.objects.get().email, "shamim@gmail.com")
        
    def test_userRegisterGenericApiView_proper_registration_and_email_verification_with_valid_otp(self):
        """test RegisterGenericApiView with all necessary info"""
        self.test_userRegistrationApiView_with_all_necessary_valid_info()
        
        """test emailVerificationApi when user will provide right otp for unverified user"""
        user = User.objects.get(email=self.data["email"]) 
        otp = OTP.objects.get(user=user) 
        data = {
            "otp": otp.code 
        } 
        response = self.client.post("/api/v1/auth/verify-email/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_verification_request_for_verified_user_with_valid_otp_that_already_used(self):
        """test RegisterGenericApiView with all necessary info"""
        self.test_userRegistrationApiView_with_all_necessary_valid_info()
        
        """test emailVerificationApi when user will provide right otp that already used. I means verified user"""
        user = User.objects.get(email=self.data["email"]) 
        otp = OTP.objects.get(user=user) 
        data = {
            "otp": otp.code 
        } 
        response = self.client.post("/api/v1/auth/verify-email/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # make a verificatioin request for a user who is already verified 
        response = self.client.post("/api/v1/auth/verify-email/", data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_userRegisterGenericApiView_proper_registration_and_email_verification_without_otp_field(self):
        """test RegisterGenericApiView with all necessary info"""
        self.test_userRegistrationApiView_with_all_necessary_valid_info()
        
        """test emailVerificationApi when user will not provide field otp"""
        data = {}
        response = self.client.post("/api/v1/auth/verify-email/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_userRegisterGenericApiView_proper_registration_and_email_verification_with_blank_otp(self):
        """test RegisterGenericApiView with all necessary info"""
        self.test_userRegistrationApiView_with_all_necessary_valid_info()
        
        """test emailVerificationApi when user will provide blank otp"""
        data = {
            "otp": "" 
        }
        response = self.client.post("/api/v1/auth/verify-email/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_userRegisterGenericApiView_proper_registration_and_email_verification_with_invalid_otp(self):
        """test RegisterGenericApiView with all necessary info"""
        self.test_userRegistrationApiView_with_all_necessary_valid_info()
        
        """test emailVerificationApi when user will provide invalid otp"""
        data = {
            "otp": "aaaaaa" 
        }
        response = self.client.post("/api/v1/auth/verify-email/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_userRegisterGenericApiView_without_email(self):
        """test the userRegisterApiView if user does not provide email"""
        data = self.data 
        data.pop("email")
        response = self.client.post(self.url, data) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_userRegisterGenericApiView_with_blank_email(self):
        """test the userRegisterApiView if user provide blank email"""
        data = self.data 
        data["email"] = "" 
        response = self.client.post(self.url, data) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
    
    def test_userRegisterGenericApiView_without_first_name(self):
        """test userRegisterApiView without first_name field"""
        data = self.data 
        data.pop("first_name") 
        response = self.client.post(self.url, data) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        
    def test_userRegisterGenericApiView_with_blank_first_name(self):
        """test userRegisterApiView with blank first_name field"""
        data = self.data 
        data["first_name"] = "" 
        response = self.client.post(self.url, data) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
    
    def test_userRegisterGenericApiView_without_last_name(self):
        """test userRegisterApiView without last_name field"""
        data = self.data 
        data.pop("last_name") 
        response = self.client.post(self.url, data) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        
    def test_userRegisterGenericApiView_with_blank_last_name(self):
        """test userRegisterApiView with blank last_name field"""
        data = self.data 
        data["last_name"] = "" 
        response = self.client.post(self.url, data) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
    
    def test_userRegisterGenericApiView_without_password(self):
        """test userRegisterApiView without password field"""
        data = self.data 
        data.pop("password") 
        response = self.client.post(self.url, data) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        
    def test_userRegisterGenericApiView_with_blank_password(self):
        """test userRegisterApiView with blank password field"""
        data = self.data 
        data["password"] = "" 
        response = self.client.post(self.url, data) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
    
    def test_userRegisterGenericApiView_without_password2(self):
        """test userRegisterApiView without password2 field"""
        data = self.data 
        data.pop("password2") 
        response = self.client.post(self.url, data) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        
    def test_userRegisterGenericApiView_with_blank_password2(self):
        """test userRegisterApiView with blank password2 field"""
        data = self.data 
        data["password2"] = "" 
        response = self.client.post(self.url, data) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
    
    def test_userRegisterGenericApiView_without_email(self):
        """test userRegisterApiView without email field"""
        data = self.data 
        data.pop("email") 
        response = self.client.post(self.url, data) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        
    def test_userRegisterGenericApiView_with_blank_email(self):
        """test userRegisterApiView with blank email field"""
        data = self.data 
        data["email"] = "" 
        response = self.client.post(self.url, data) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        
    def test_userRegisterGenericApiView_with_invalid_email(self):
        """test userRegisterApiView with invalid email field"""
        data = self.data 
        data["email"] = "invalid_email" 
        response = self.client.post(self.url, data) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
    
    def test_userLoginGenericApiView_with_valid_login_credentials(self):
        """test user login view with all necessary valid credentials"""
        # proper registration and email verification 
        self.test_userRegisterGenericApiView_proper_registration_and_email_verification_with_valid_otp()
        
        data = {
            "email": "shamim@gmail.com", 
            "password": "test1234"
        }
        response = self.client.post("/api/v1/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
    
    def test_userLoginGenericApiView_without_password_field(self):
        """test user login view without password field"""
        # proper registration and email verification 
        self.test_userRegisterGenericApiView_proper_registration_and_email_verification_with_valid_otp()
        
        data = {
            "email": "shamim@gmail.com", 
        }
        response = self.client.post("/api/v1/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 
    
    def test_userLoginGenericApiView_with_wrong_password(self):
        """test user login view with wrong password"""
        # proper registration and email verification 
        self.test_userRegisterGenericApiView_proper_registration_and_email_verification_with_valid_otp()
        
        data = {
            "email": "shamim@gmail.com", 
            "password": "wrong_password"
        }
        response = self.client.post("/api/v1/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 
    
    def test_userLoginGenericApiView_with_blank_email(self):
        """test user login view with empty '' email"""
        # proper registration and email verification 
        self.test_userRegisterGenericApiView_proper_registration_and_email_verification_with_valid_otp()
        
        data = {
            "email": "", 
            "password": "test1234"
        }
        response = self.client.post("/api/v1/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 
    
    def test_userLoginGenericApiView_without_email(self):
        """test user login view without email field"""
        # proper registration and email verification 
        self.test_userRegisterGenericApiView_proper_registration_and_email_verification_with_valid_otp()
        
        data = {
            "password": "test1234"
        }
        response = self.client.post("/api/v1/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 
    
    def test_userLoginGenericApiView_with_invalid_email(self):
        """test user login view with invalid email"""
        # proper registration and email verification 
        self.test_userRegisterGenericApiView_proper_registration_and_email_verification_with_valid_otp()
        
        data = {
            "email": "not_a_valid_email", 
            "password": "test1234"
        }
        response = self.client.post("/api/v1/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 