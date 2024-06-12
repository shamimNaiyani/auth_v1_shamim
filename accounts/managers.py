from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _ 


class UserManager(BaseUserManager):
    def email_validators(self, email: str) -> str:
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(_("Please enter valid email address!"))
    
    def create_user(self, email: str, password: str, first_name: str, last_name: str, **extra_fields):
        if email:
            # to prevent multiple signup with same email
            email = self.normalize_email(email) 
            # if email is not vaild this below line will raise an email validation errors
            self.email_validators(email)
        else:
            raise ValueError("Email is required!")

        # user provide valid email 
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        # I do not save the password directly in the database 
        # I set the password here. Because BaseUserManager will perform necessary 
        # encription staff on the password 
        user.set_password(password)
        # save the user in the default database
        user.save(using=self._db)
        return user 
    
    def create_superuser(self, email: str, password: str, first_name: str, last_name: str, **extra_fields):
        # super user should have all permission over the system 
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if not extra_fields.get("is_staff"):
            raise ValueError(_("is staff must be true for admin user"))
        
        if not extra_fields.get("is_superuser"):
            raise ValueError(_("is superuser must be true for admin user"))
        
        if not extra_fields.get("is_verified"):
            raise ValueError(_("if verified must be true for admin user"))
        
        superuser = self.create_user(email, password, first_name, last_name, **extra_fields)
        superuser.save(using=self._db)
        return superuser 
        
        
        