import datetime
import requests
import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/gmail.send']
  # VERSE_API_URL = 'https://example.com/api/verses'  # Replace with the URL of a verse API

    

VERSE_API_URL = 'https://beta.ourmanna.com/api/v1/get?format=json&order=daily'

headers = {"accept": "application/json"}

response = requests.get(VERSE_API_URL, headers=headers)

print(response.text)

SENDER_EMAIL = 'byenna21@gmail.com'             # Replace with your Gmail address
RECEIVER_EMAIL = 'byenna21@gmail.com'      # Replace with the recipient's Gmail address
TIME = '08:00'                                   # Specify the time you want to receive the verse

def main():
       creds = None
       if os.path.exists('token.json'):
           creds = Credentials.from_authorized_user_file('token.json', SCOPES)
       if not creds or not creds.valid:
           if creds and creds.expired and creds.refresh_token:
               creds.refresh(Request())
           else:
               flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
               creds = flow.run_local_server(port=0)
           with open('token.json', 'w') as token:
               token.write(creds.to_json())
       current_time = datetime.datetime.now().strftime("%H:%M")
       if current_time == TIME:
           verse = requests.get(VERSE_API_URL).json()['verse']
           message = f"Subject: Daily Verse\n\n{verse}"
           service = build('gmail', 'v1', credentials=creds)
           service.users().messages().send(userId='me', body={'raw': base64.urlsafe_b64encode(message.encode()).decode()}).execute()

if __name__ == '__main__':
       while True:
           main()