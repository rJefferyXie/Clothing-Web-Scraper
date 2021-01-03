from __future__ import print_function
import pickle
import os.path
from pygdrive3 import service as service3
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# This file was setup using google's quickstart documentation posted below:
# https://developers.google.com/drive/api/v3/quickstart/python?authuser=1


def authenticate():
    """
    Authenticate the user and allow them access to the google drive.
    :return: A service object used to communicate with google's API
    """

    scopes = ['https://www.googleapis.com/auth/drive']
    credentials = None

    # Create the user's access and refresh tokens for the first time that this program is run
    if os.path.exists('credentials/token.pickle'):
        with open('credentials/token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/client_secrets.json', scopes)
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('credentials/token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    return build('drive', 'v3', credentials=credentials)


def update_storage(service, filenames):
    """
    Update the storage folder in our google drive.
    :param service: A service object used to communicate with google's API
    :param filenames: A list of the filenames in cache_storage
    :return: None
    """
    # Create a list of {file names, file ids}
    results = service.files().list(
        pageSize=50, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])[1:-1]

    # Deleting every file and folder in the google drive
    try:
        for item in items:
            service.files().delete(fileId=item['id']).execute()
    except IndexError:
        pass

    # Log in to the pydrive3 client to upload files
    drive_service = service3.DriveService('client_secrets.json')
    drive_service.auth()

    folders = drive_service.list_folders_by_name("storage")

    # Upload the new data to the storage in google drive
    for filename in filenames:
        test_file = drive_service.upload_file(filename, "cache_storage/" + filename, folders[0]['id'])
        drive_service.anyone_permission(test_file)


def main():
    """
    Authenticate to google drive servers and update the storage.
    :return: None
    """
    file_names = ["accessories_men_cache.csv",
                  "accessories_women_cache.csv",
                  "bottoms_men_cache.csv",
                  "bottoms_women_cache.csv",
                  "footwear_men_cache.csv",
                  "footwear_women_cache.csv",
                  "overall_men_cache.csv",
                  "overall_women_cache.csv",
                  "tops_men_cache.csv",
                  "tops_women_cache.csv"
                  ]
    service = authenticate()
    update_storage(service, file_names)


if __name__ == '__main__':
    main()
