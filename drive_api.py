import os
import os.path
import io

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

#from Google import Create_Service
from googleapiclient.http import MediaIoBaseDownload


SCOPES = ["https://www.googleapis.com/auth/drive"]

API_NAME = 'drive'
API_VERSION = 'v3'

class AutorizationError(Exception):
    def __init__(self, drive_dir):
        self.drive_dir = drive_dir

    def __str__(self):
        return f"Authorization error - cannot find {self.drive_dir}/credentials.json"


class GoogleDriveAPI():
    def __init__(self):
        self.creds = None
        self.service = None

        self.database_dir = "databases"
        self.database_gdrive_dir = "game_catalog_database"
        self.drive_api_dir = "drive_api"

    def build_service(self):
        if not self.creds == None:
            self.service = build(API_NAME, API_VERSION, credentials=self.creds)
        else:
            print("The application has not been authorized")

    def autorize_app(self):
        # Authorization
        if not os.path.exists(self.drive_api_dir):
            os.mkdir(self.drive_api_dir)

        if os.path.exists(f"{self.drive_api_dir}/credentials.json"):
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
        
            self.build_service()
        else:
            print(f"Authorization error - cannot find {self.drive_api_dir}/credentials.json")
            raise AutorizationError(self.drive_api_dir)

    def create_folder_on_gdrive(self):
        file_metadata = {
            "name": self.database_gdrive_dir,
            'mimeType': "application/vnd.google-apps.folder"
        }

        file = self.service.files().create(body=file_metadata, fields="id").execute()

        return file.get('id')
    
    def get_folder_id(self):
        response = self.service.files().list(
            q=f"name='{self.database_gdrive_dir}' and mimeType='application/vnd.google-apps.folder' and trashed = false",
            spaces='drive'
        ).execute()

        # Creating the folder if not exists on Google Drive
        if not response['files']:
            return None
        else:
            return response['files'][0]['id']

    def get_files_list(self, folder_id):
        response = self.service.files().list(q=f"'{folder_id}' in parents and trashed=false", 
                                        fields="files(id, name)").execute()
        files = response.get('files', [])
        print(f"Znaleziono {len(files)} plików w folderze {self.database_gdrive_dir}.")

        return files

    def upload_files(self):
        try:
            self.autorize_app()
            try:
                folder_id = self.get_folder_id()
                #Creating folder if doesnt exist
                if folder_id == None:
                    folder_id = self.create_folder_on_gdrive()

                #Uploading data from computer
                for file in os.listdir(self.database_dir):
                    # Sprawdzenie, czy plik o tej samej nazwie istnieje w folderze
                    existing_files = self.service.files().list(
                        q=f"name='{file}' and '{folder_id}' in parents",
                        spaces='drive'
                    ).execute()

                    # Jeśli plik istnieje, usuwamy go, aby nadpisać
                    if existing_files['files']:
                        for existing_file in existing_files['files']:
                            self.service.files().delete(fileId=existing_file['id']).execute()

                    file_metadata = {
                        "name": file,
                        "parents": [folder_id]
                    }

                    media = MediaFileUpload(f"{self.database_dir}/{file}")
                    upload_file = self.service.files().create(body=file_metadata,
                                                        media_body = media,
                                                        fields = "id").execute()
                    print("Uploaded file: " + file)

            except HttpError as e:
                print("Error: " + str(e))
        except AutorizationError as e:
            print(e)

    def download_files(self):
        try:
            self.autorize_app()
            folder_id = self.get_folder_id()

            if not folder_id == None:
                files = self.get_files_list(folder_id)

                if not os.path.exists(self.database_dir):
                    os.mkdir(self.database_dir)         

                for file in files:
                    print(f"Pobieranie pliku: {file['name']} (ID: {file['id']})")
                    request = self.service.files().get_media(fileId=file['id'])


                    with io.FileIO(os.path.join(self.database_dir, file['name']), "wb") as fh:
                        downloader = MediaIoBaseDownload(fh, request)
                        done = False
                        while not done:
                            status, done = downloader.next_chunk()
                            print(f"Pobieranie: {int(status.progress() * 100)}%")
                    
                    print(f"Plik pobrany jako: {self.database_dir}/{file['name']}")
            else:
                print("Folder nie istnieje!")

        except AutorizationError as e:
            print(e)