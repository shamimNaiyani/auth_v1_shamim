from accounts.models import User
from django.contrib.auth import authenticate

def register_social_user(provider, email, first_name, last_name):
    old_user = User.objects.filter(email=email)
    if old_user.exists():
        if old_user.exists():
            if provider == old_user[0].auth_provider:
                register_user = authenticate(email=email, password=settings.SOCIAL_AUTH_PASSWORD) 
                tokens = register_user.tokens()
                
                return {
                    'full_name': register_user.get_username,
                    'email': register_user.email,
                    "access_token":str(tokens.get('access')),
                    "refresh_token":str(tokens.get('refresh'))
                }
    else:
        new_user = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password': settings.SOCIAL_AUTH_PASSWORD 
        }
        user = User.objects.create_user(**new_user)
        user.auth_provider = provider 
        user.is_verified = True 
        user.save()
        login_user = authenticate(email=email, password=settings.SOCIAL_AUTH_PASSWORD)
        
        tokens = login_user.tokens()
        
        return {
            'email':login_user.email,
            'full_name': login_user.get_username,
            'access_token': str(tokens.get('access')),
            'refresh_token': str(tokens.get('refresh'))
        }