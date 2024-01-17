import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request 

# Set your Google Drive folder ID
folder_id = 'XXXXXXXXXX' #ID de la carpeta en google drive

# Set the scopes for accessing Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def authenticate_google_drive():
    creds = None
    token_path = r'C:\XXXXXXXXXXXX\token.json'  # Replace with the actual path to your token file
    credentials_path = r'C:\XXXXXXXXXXXX\credentials.json'  # Replace with your actual credentials file

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Load the client ID and secret from the credentials file
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES, redirect_uri='http://localhost:8888/'
            )
            creds = flow.run_local_server(port=0)

        # Save the obtained credentials to the token file
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds

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
                # Recursively count files and folders in subfolders
                subfolder_id = file['id']
                subfolder_file_count, subfolder_folder_count = count_files_and_folders_in_folder(service, subfolder_id)
                file_count += subfolder_file_count
                folder_count += subfolder_folder_count
            else:
                file_count += 1

        page_token = results.get('nextPageToken')
        if not page_token:
            break

    return file_count, folder_count

def main():
    creds = authenticate_google_drive()
    service = build('drive', 'v3', credentials=creds)

    # Replace 'YOUR_FOLDER_ID' with the actual Google Drive folder ID
    folder_id = 'XXXXXXXXXXXXXXXXXXXXXX'#ID de la carpeta en google drive

    file_count, folder_count = count_files_and_folders_in_folder(service, folder_id)
    print(f'The folder and its subfolders contain {file_count} files and {folder_count} folders.')

if __name__ == '__main__':
    main()
