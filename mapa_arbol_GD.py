import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Set your Google Drive folder ID
folder_id = 'XXXXXXXXXXXXXXXXXXX' #usar el ID del folder de Google drive

# Set the scopes for accessing Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def authenticate_google_drive():
    creds = None
    token_path = r'token.json' #Definir la ruta donde se guarda el archivo token.json
    credentials_path = r'credentials.json' #Definir la ruta donde se guarda el archivo token.json

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES, redirect_uri='http://localhost:8888/'
            )
            creds = flow.run_local_server(port=0)

        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds

def print_google_drive_structure_with_file_count(service, folder_id, indent="", file=None):
    file_count, folder_count = count_files_and_folders_in_folder(service, folder_id)

    print(f"{indent}{get_folder_name(service, folder_id)} ({file_count} Archivos)", file=file)

    subfolders = get_subfolders(service, folder_id)
    for subfolder_id in subfolders:
        print_google_drive_structure_with_file_count(service, subfolder_id, indent + "│   ", file=file)

def get_subfolders(service, folder_id):
    subfolders = []
    results = service.files().list(
        q=f"'{folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'",
        fields="files(id)"
    ).execute()

    subfolders.extend([file['id'] for file in results.get('files', [])])
    return subfolders

def get_folder_name(service, folder_id):
    file_metadata = service.files().get(fileId=folder_id, fields="name").execute()
    return file_metadata.get('name', '')

def count_files_and_folders_in_folder(service, folder_id):
    file_count = 0
    folder_count = 0

    page_token = None
    while True:
        results = service.files().list(
            q=f"'{folder_id}' in parents",
            fields="files(id, mimeType), nextPageToken",
            pageToken=page_token
        ).execute()

        files = results.get('files', [])
        for file in files:
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                folder_count += 1
            else:
                file_count += 1

        page_token = results.get('nextPageToken')
        if not page_token:
            break

    return file_count, folder_count

def save_structure_to_file(file_path, service, folder_id):
    with open(file_path, 'w', encoding='utf-8') as file:
        print_google_drive_structure_with_file_count(service, folder_id, file=file)

def main():
    creds = authenticate_google_drive()
    service = build('drive', 'v3', credentials=creds)

    folder_id = 'XXXXXXXXXXXXXXXXXXX' #usar el ID del folder de Google drive
    save_structure_to_file('nombre archivo', service, folder_id) #definir el nombre y ubicación del archivo de salida

if __name__ == '__main__':
    main()