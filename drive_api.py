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

# FROM TUTORIAL
API_NAME = 'drive'
API_VERSION = 'v3'
# ***********


class AutorizationError(Exception):
    def __init__(self, drive_dir):
        self.drive_dir = drive_dir

    def __str__(self):
        return f"Authorization error - cannot find {self.drive_dir}/credentials.json"


class GoogleDriveAPI():
    def __init__(self):
        self.creds = None

        self.database_dir = "databases"
        self.database_gdrive_dir = "game_catalog_database"
        self.drive_api_dir = "drive_api"

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
        else:
            #print(f"Authorization error - cannot find {self.drive_api_dir}/credentials.json")
            raise AutorizationError(self.drive_api_dir)

    def upload_files(self):
        try:
            self.autorize_app()
            try:
                service = build(API_NAME, API_VERSION, credentials=self.creds)
                
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
                    # Sprawdzenie, czy plik o tej samej nazwie istnieje w folderze
                    existing_files = service.files().list(
                        q=f"name='{file}' and '{folder_id}' in parents",
                        spaces='drive'
                    ).execute()

                    # Jeśli plik istnieje, usuwamy go, aby nadpisać
                    if existing_files['files']:
                        for existing_file in existing_files['files']:
                            service.files().delete(fileId=existing_file['id']).execute()

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
        except AutorizationError as e:
            print(e)

    def download_files(self):
        #service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        try:
            self.autorize_app()
            service = build(API_NAME, API_VERSION, credentials=self.creds)
                
            #Find folder id by name
            response = service.files().list(
                q=f"name = '{self.database_gdrive_dir}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false",
                fields = "files(id, name)"
            ).execute()
            folders = response.get('files')
            if not folders:
                print("Folder o podanej nazwie nie został znaleziony.")
                return None
            folder_id =  folders[0]['id'] 

            #Find list of files in the folder
            response = service.files().list(q=f"'{folder_id}' in parents and trashed=false", 
                                            fields="files(id, name)").execute()
            files = response.get('files', [])
            print(f"Znaleziono {len(files)} plików w folderze {self.database_gdrive_dir}.")

            if not os.path.exists(self.database_dir):
                os.mkdir(self.database_dir)         

            for file in files:
                print(f"Pobieranie pliku: {file['name']} (ID: {file['id']})")
                request = service.files().get_media(fileId=file['id'])


                with io.FileIO(os.path.join(self.database_dir, file['name']), "wb") as fh:
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while not done:
                        status, done = downloader.next_chunk()
                        print(f"Pobieranie: {int(status.progress() * 100)}%")
                
                print(f"Plik pobrany jako: {self.database_dir}/{file['name']}")




        except AutorizationError as e:
            print(e)


drive = GoogleDriveAPI()
drive.upload_files()
#drive.download_files()