from django.core.mail import EmailMessage 
from rest_framework_authentication import settings


def successful_payment_email():
    print("Hello admin! I send the email to the users!")
    
    send_email = EmailMessage(
        subject="Payment Successful 🥰!",
        to=["testemail@gmail.com"],
        from_email=settings.DEFAULT_FROM_EMAIL, 
        body="Hi there! Your payment has been done! Thanks for being with Naiyani Inc. Enjoy your journey with Naiyani!",
    )
    
    send_email.send(fail_silently=True) 
    