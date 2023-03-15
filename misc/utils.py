import os
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from django.core.cache import cache

def get_google_credentials(request):
    user_id = str(request.user.id)
    credentials_json = cache.get(user_id)
    if credentials_json:
        return Credentials.from_authorized_user_info(info=credentials_json)
    return None

def store_google_credentials(request, credentials):
    user_id = str(request.user.id)
    credentials_json = credentials.to_authorized_user_info()
    cache.set(user_id, credentials_json)
    
def generate_google_url(request):
    redirect_uri = os.getenv('GOOGLE_REDIRECT_URI')
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    scope = os.getenv('GOOGLE_FIT_SCOPE')

    flow = InstalledAppFlow.from_client_config(
    client_config={
        'installed': {
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uris': [redirect_uri],
            'auth_uri': os.getenv('GOOGLE_AUTH_URI'),
            'token_uri': os.getenv('GOOGLE_TOKEN_URI')
        }
    },
    scopes=scope,
    redirect_uri=redirect_uri
    )
    authorization_url, _ = flow.authorization_url(prompt='consent')
    auth_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    request.session['google_auth_state'] = state
    dd(authorization_url);
    return authorization_url
