import os
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]

class gdrive():
    def __init__(self):
        self.creds = None

        self.database_dir = "databases"
        self.database_gdrive_dir = "game_catalog_database"
        self.drive_api_dir = "drive_api"

    def autorization(self):
        # Authorization
        if os.path.exists(f'{self.drive_api_dir}/token.json'):
            self.creds = Credentials.from_authorized_user_file(f"{self.drive_api_dir}/token.json", SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    f"{self.drive_api_dir}/credentials.json", SCOPES)
                self.creds = flow.run_local_server(port=0)

        with open(f'{self.drive_api_dir}/token.json', 'w') as token:
            token.write(self.creds.to_json())

    def upload(self):
        self.autorization()
        try:
            service = build("drive", 'v3', credentials=self.creds)
            
            #Checking if the folder exists on Google Drive
            response = service.files().list(
                q=f"name='{self.database_gdrive_dir}' and mimeType='application/vnd.google-apps.folder'",
                spaces='drive'
            ).execute()

            # Creating the folder if not exists on Google Drive
            if not response['files']:
                file_metadata = {
                    "name": self.database_gdrive_dir,
                    'mimeType': "application/vnd.google-apps.folder"
                }

                file = service.files().create(body=file_metadata, fields="id").execute()

                #Getting folder_id of created folder
                folder_id = file.get('id')
            
            #Getting folder_id if folder exists 
            else:
                folder_id = response['files'][0]['id']


            #Uploading data from computer
            for file in os.listdir(self.database_dir):
                file_metadata = {
                    "name": file,
                    "parents": [folder_id]
                }

                media = MediaFileUpload(f"{self.database_dir}/{file}")
                upload_file = service.files().create(body=file_metadata,
                                                    media_body = media,
                                                    fields = "id").execute()
                print("Uploaded file: " + file)

        except HttpError as e:
            print("Error: " + str(e))


drive = gdrive()
drive.upload()