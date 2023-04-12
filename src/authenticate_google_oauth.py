import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def oauth_google(service):
    if service == 'image_search':
        return build('customsearch', 'v1', developerKey='APIトークン')
    elif service == 'gdrive':
        credential = None
        if os.path.exists('token.json'):
            credential = Credentials.from_authorized_user_file('token.json', ['SCOPE'])

        if not credential or not credential.valid:
            if credential and credential.expired and credential.refresh_token:
                credential.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['SCOPE'])
                credential = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(credential.to_json())

        return build('drive', 'v3', credentials=credential)
