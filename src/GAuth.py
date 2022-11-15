from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
# https://developers.google.com/identity/protocols/oauth2/scopes#youtube
SCOPES = [
    'https://www.googleapis.com/auth/youtube', 
    'https://www.googleapis.com/auth/youtube.force-ssl'
]

INSTANCE = None

# Need to get this for your service in the Google Admin Console.
CLIENT_SECRET_PATH = 'credentials/client_secret.json'

# This will be created when you first run this app after login and permission screen.
TOKEN_FILE_PATH = './credentials/token.json'

class GAuth:
    
    def __init__(self, scopes) -> None:
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        self.creds = None
        self.scopes = scopes
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(TOKEN_FILE_PATH):
            self.creds = Credentials.from_authorized_user_file(TOKEN_FILE_PATH, self.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(TOKEN_FILE_PATH, 'w') as token:
                token.write(self.creds.to_json())

    def get_creds(self):
        return self.creds

    @staticmethod
    def default():
        return GAuth(SCOPES)
