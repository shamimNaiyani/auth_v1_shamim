from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _ 
from .managers import UserManager
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True, verbose_name=_("Email")) 
    first_name = models.CharField(max_length=50, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=25, verbose_name=_("Last Name"))
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    # user name field for login: set email as a username 
    USERNAME_FIELD = "email" 
    
    # required fields for registration 
    REQUIRED_FIELDS = ["first_name", "last_name"]
    
    # UserManager Object will take care everything about this user 
    objects = UserManager()
    
    @property 
    def get_user_fullname(self):
        return f"{self.first_name} {self.last_name}" 

    @property
    def get_user_refresh_and_access_token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    # string representation in the admin panel 
    def __str__(self):
        return self.email
    

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    
    def __str__(self):
        return f"{self.user.first_name}-passcode" 