from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def auth():
    creds = None
   
   
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
  
  
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
      
      
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_service():
   
    creds = auth()

    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service
    
    

def list_files():
    drive_service = get_service()
    results = drive_service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

def upload_file(filepath, filename, folder_id=None):
    drive_service = get_service()
    if folder_id:
        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }
    else:
        file_metadata = {'name': filename}
        
    media = MediaFileUpload(filepath, mimetype='image/jpeg')
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    

def create_folder(name):
    drive_service = get_service()
    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()

