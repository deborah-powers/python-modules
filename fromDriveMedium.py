#!/usr/bin/python3.10
# -*- coding: utf-8 -*-

import os
import io
import re

from google.auth.transport.requests import Request # type: ignore
from google.oauth2.credentials import Credentials # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore
from googleapiclient.discovery import build # type: ignore
from googleapiclient.http import MediaIoBaseDownload # type: ignore

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Hard-coded inputs
DRIVE_URL = 'https://drive.google.com/drive/folders/1eHdmkbaVUtHaTV-mMWn3N5h4KR_FGnDc'

OUTPUT_FOLDER = 'Z:/GDRIVE/'

def authenticate():
    """Authenticate the user and return the service object."""
    creds = None
    credentials_path = 'credentials.json'
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('drive', 'v3', credentials=creds)
    return service

def extract_file_id(drive_url):
    """Extract the folder ID from a Google Drive folder URL."""
    match = re.search(r'/folders/([a-zA-Z0-9_-]+)', drive_url)
    if not match:
        raise ValueError('Invalid Google Drive folder URL')
    return match.group(1)

def download_files_recursive(service, folder_id, output_folder,log_file):
    """Download all files in a folder recursively."""
    files,total_pages = list_files_in_folder(service, folder_id)
    for file in files:
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            # If it's a folder, recursively download its contents
            subfolder_id = file['id']
            subfolder_name = file['name']
            subfolder_output_folder = os.path.join(output_folder, subfolder_name)
            os.makedirs(subfolder_output_folder, exist_ok=True)
            download_files_recursive(service, subfolder_id, subfolder_output_folder,log_file)
        else:
            # If it's a file, download it
            download_file(service, file['id'], output_folder,log_file,total_pages)

def download_file(service, file_id, output_folder,log_file,total_pages):
    """Download a file by its file ID."""
    file_metadata = service.files().get(fileId=file_id).execute()
    file_name = file_metadata['name']
    try:
        print("file_metadatafile_metadata",file_metadata)        
        
        # Check if the file is a Google Docs Editors file
        if file_metadata['mimeType'] == 'application/vnd.google-apps.document':
            # Export the Google Docs file as a PDF
            request = service.files().export_media(fileId=file_id, mimeType='application/pdf')
        elif file_metadata['mimeType'] == 'application/vnd.google-apps.spreadsheet':
            # Export the Google Sheets file as an Excel file
            request = service.files().export_media(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        elif file_metadata['mimeType'] == 'application/vnd.google-apps.presentation':
            # Export the Google Slides file as a PowerPoint file
            request = service.files().export_media(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.presentationml.presentation')
        else:
            # For other file types, download as is
            request = service.files().get_media(fileId=file_id)

        file_path = os.path.join(output_folder, file_name)
        os.makedirs(output_folder, exist_ok=True)  # Ensure the output directory exists
        with io.FileIO(file_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}% complete.")
                print("done",done)
        #print(f"File downloaded to {file_path}")
        # Log file path and download status to the log file
        with open(log_file, 'a') as log:
            log.write(f"'Page No: '{total_pages} FilePath: {file_path},{'Downloaded' if done else 'Not Downloaded'}\n")
        
        print(f"File downloaded to {file_path}")
    except Exception as e:
        print(f"Error downloading file: {e}")
        # Log error message to the log file
        with open(log_file, 'a') as log:
            log.write(f"Error downloading file: PageNo:::: {total_pages} {file_name}, {str(e)}\n")

def list_files_in_folder(service, folder_id):
    """List all files in a folder."""
    files = []
    page_token = None
    page_number = 1  # Initialize page number
    print("List all files in a folder")
    while True:
        request = service.files().list(
            q=f"'{folder_id}' in parents",
            fields='nextPageToken, files(id, name,mimeType)',
            #pageToken=page_token,
            pageToken=None if page_number == 1 else page_token,
            pageSize=1000  # You can adjust the page size as needed
        )
        response = request.execute()

        # Extract files from the response
        files.extend(response.get('files', []))

        # Check if there are more pages to retrieve
        page_token = response.get('nextPageToken')
        if not page_token:
            break

        # Increment the page number
        page_number += 1

    return files,page_number

def download_files_in_folder(service, folder_id, output_folder):
    """Download all files in a folder."""
    files,total_pages = list_files_in_folder(service, folder_id)
    print(f"Downloading files from folder with ID: {folder_id} to {output_folder}...")
    for file in files:
        download_file(service, file['id'], output_folder)

def main():
    service = authenticate()
    file_id = extract_file_id(DRIVE_URL)
    log_file = 'Z:/GDRIVE/DownloadFilesDetails.txt'
    print(f"Downloading file with ID: {file_id} to {OUTPUT_FOLDER}...")
    download_files_recursive(service, file_id, OUTPUT_FOLDER,log_file)

if __name__ == '__main__':
    main()

"""
source: https://medium.com/@aalam-info-solutions-llp/downloading-files-from-google-drive-link-to-a-target-folder-using-python-93b8c67f1304
auteur: https://aalamsoft.com/
"""