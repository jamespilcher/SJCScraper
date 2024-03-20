from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
TOKEN_CACHE = 'caches/token_cache.pkl'
CREDENTIALS_JSON = os.getenv('GOOGLE_OAUTH_CREDENTIALS_PATH', 'credentials.json')
def authenticate():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    if os.path.exists(TOKEN_CACHE):
        with open(TOKEN_CACHE, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_JSON,  
                SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_CACHE, 'wb') as token:
            pickle.dump(creds, token)
    return creds