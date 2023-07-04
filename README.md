# daily_verse_emailer
A Project idea for sending a daily verse to your Google Mail account.

Description: In this project, you will create a Python script that sends a verse to your Google Mail every day at a specified time using the Gmail API and a verse API.
Requirements:
1. Python installed on your system.
2. Access to the internet.
3. A Google account with Gmail enabled.
Steps:
1. Set up a new project in the Google Cloud Console:
   a. Go to https://console.cloud.google.com/.
   b. Create a new project.
   c. Enable the Gmail API for the project.
   d. Generate credentials (OAuth client ID) for the project.
2. Install the required packages:
   a. Install the Google Client Library by running the following command in your terminal:
      `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`
   b. Install the Requests library by running:
      `pip install requests`
3. Create a Python script and import the necessary libraries:

   import datetime
   import requests
   from google.oauth2.credentials import Credentials
   from google_auth_oauthlib.flow import InstalledAppFlow
   from google.auth.transport.requests import Request

4. Define the necessary variables:

   SCOPES = ['https://www.googleapis.com/auth/gmail.send']
   VERSE_API_URL = 'https://example.com/api/verses'  # Replace with the URL of a verse API
   SENDER_EMAIL = 'your-email@gmail.com'             # Replace with your Gmail address
   RECEIVER_EMAIL = 'recipient-email@gmail.com'      # Replace with the recipient's Gmail address
   TIME = '15:00'                                   # Specify the time you want to receive the verse

5. Implement the main functionality:

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

6. Run the script periodically:

   if __name__ == '__main__':
       while True:
           main()


7. Replace the `VERSE_API_URL` variable with the actual URL of an API that provides daily verses. You can search for available verse APIs and choose one that suits your preference.
8. Replace the `SENDER_EMAIL` and `RECEIVER_EMAIL` variables with your email address and the recipient's email address, respectively.
9. Specify the desired time to receive the verse in the `TIME` variable. The script will check the time every minute and send the verse when the specified time is reached.
10. Save the script with a `.py` extension (e.g., `daily_verses.py`).
11. Run the script in your terminal using the command:
    `python daily_verses.py`
The script will continue running until you stop it manually. Ensure that your system is connected to the internet during that time. You will receive a daily verse at the specified time in your Google Mail inbox.
Note: Make sure to follow the API usage policies of the verse API you choose and respect any rate limits they have in place.