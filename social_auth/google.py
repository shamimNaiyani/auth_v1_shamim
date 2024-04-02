import requests
from google.oauth2 import id_token 


class Google():
    @staticmethod
    def validate(access_token):
        try:
            id_info = id_token.verify_oauth2_token(access_token, requests.Request()) 
            if 'accounts.google.com' in id_info['iss']:
                return id_info 
        except:
            return 'The token is either invalid or expired!'