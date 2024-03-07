from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from rest_framework_authentication import settings
from otp_generator.otp import generate_otp
from .models import User, OTP


def send_otp_to_new_registered_user(request, email):
    # generate 6 digits otp
    otp = generate_otp(6) 
    print(otp)
    
    # email subject 
    subject = "Account verification: One time passcode (OTP) for email varification"
    user = User.objects.get(email=email)
    # find the requested site domain using get_current_site method 
    current_site = get_current_site(request=request).domain
    email_body = f"Hi {user.first_name}! Thanks for signing up on {current_site}. Please verify your email with the \n one time pass code.\nYour OTP is {otp}"
    from_email = settings.DEFAULT_FROM_EMAIL
    send_email = EmailMessage(
        subject=subject, 
        body=email_body, 
        from_email=from_email, 
        to=[user.email]
    )
    
    # send the email 
    send_email.send(fail_silently=True)
    # save the token to the database 
    OTP.objects.create(user=user, code=otp)
    

def send_reset_password_link_to_email(data): 
    
    email = EmailMessage(
        subject=data["subject"], 
        body=data["body"], 
        from_email=settings.DEFAULT_FROM_EMAIL, 
        to=[data["to_email"]]
    )
    
    email.send(fail_silently=True)


def send_new_password_to_email(data):
    email = EmailMessage(
        subject=data["subject"],
        body=data["body"],
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[data["to"]]
    )
    
    email.send(fail_silently=True)