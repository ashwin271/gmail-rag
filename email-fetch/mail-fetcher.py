import os.path
import base64
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
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
    return build('gmail', 'v1', credentials=creds)

def get_email_content(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        payload = message['payload']
        headers = payload['headers']
        
        subject = next(header['value'] for header in headers if header['name'] == 'Subject')
        sender = next(header['value'] for header in headers if header['name'] == 'From')
        date = next(header['value'] for header in headers if header['name'] == 'Date')

        parts = payload.get('parts', [])
        body = ""
        if 'body' in payload:
            body = payload['body'].get('data', '')
        elif parts:
            part = parts[0]
            body = part['body'].get('data', '')

        if body:
            body = base64.urlsafe_b64decode(body).decode('utf-8')

        return {
            'id': msg_id,
            'subject': subject,
            'sender': sender,
            'date': date,
            'body': body
        }
    except Exception as error:
        print(f'An error occurred: {error}')
        return None

def fetch_all_emails(service, user_id='me', query=''):
    try:
        results = service.users().messages().list(userId=user_id, q=query).execute()
        messages = results.get('messages', [])
        
        emails = []
        for message in messages:
            email_data = get_email_content(service, user_id, message['id'])
            if email_data:
                emails.append(email_data)
        
        return emails
    except HttpError as error:
        print(f'An error occurred: {error}')
        return []

def save_emails_to_file(emails, filename='emails.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(emails, f, ensure_ascii=False, indent=4)

def main():
    service = get_gmail_service()
    emails = fetch_all_emails(service)
    save_emails_to_file(emails)
    print(f'Saved {len(emails)} emails to emails.json')

if __name__ == '__main__':
    main()