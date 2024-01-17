import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import matplotlib.pyplot as plt

# Set your Google Drive folder ID
folder_id = 'XXXXXXXXXXXXXXXXXXXXXX' #ID de la carpeta de Google Drive

# Set the scopes for accessing Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def authenticate_google_drive():
    creds = None
    token_path = r'token.json'  # Replace with the actual path to your token file
    credentials_path = r'credentials.json'  # Replace with your actual credentials file
  

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

def calculate_size_of_folder_contents(service, folder_id):
    total_size = 0

    results = service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name, mimeType, size)"
    ).execute()

    files = results.get('files', [])
    for file in files:
        if file['mimeType'] != 'application/vnd.google-apps.folder':
            total_size += int(file['size']) if 'size' in file else 0

    return total_size

def calculate_sizes_of_children_folders(service, folder_id):
    sizes = {}

    results = service.files().list(
        q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder'",
        fields="files(id, name)"
    ).execute()

    folders = results.get('files', [])
    for folder in folders:
        folder_id = folder['id']
        folder_name = folder['name']
        folder_size = calculate_size_of_folder_contents(service, folder_id)
        sizes[folder_name] = folder_size

    return sizes

def plot_sizes(sizes):
    fig, ax = plt.subplots()
    
    folders = list(sizes.keys())
    sizes_values = list(sizes.values())

    ax.barh(folders, sizes_values)
    ax.set_xlabel('Size (bytes)')
    ax.set_ylabel('Folder')
    ax.set_title('Sizes of Immediate Children Folders')

    plt.show()

def main():
    creds = authenticate_google_drive()
    service = build('drive', 'v3', credentials=creds)

    # Replace 'YOUR_FOLDER_ID' with the actual Google Drive folder ID
    folder_id = 'XXXXXXXXXXXXXXXXXXXXXX' #ID de la carpeta de Google Drive

    sizes = calculate_sizes_of_children_folders(service, folder_id)
    print(f'Sizes of Immediate Children Folders: {sizes}')

    plot_sizes(sizes)

if __name__ == '__main__':
    main()