from __future__ import print_function
import os.path
from io import open
from io import BytesIO
from googleapiclient.http import MediaIoBaseDownload
from google_drive import authenticate


def download(service):
    """
    Download files from google drive into our directory called cache_storage.
    Creates cache_storage if not already present.
    :param service: A service object used to communicate with google's API
    :return: None
    """

    # Create a list of {file names, file ids}
    results = service.files().list(
        pageSize=50, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])[1:-1]

    # Create cache_storage if not already present
    if not os.path.exists("cache_storage/"):
        os.mkdir("cache_storage/")

    # Download each item and put them in cache_storage
    for item in items:
        request = service.files().get_media(fileId=item["id"])
        fh = BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        with open("cache_storage/" + item["name"], "wb") as f:
            fh.seek(0)
            f.write(fh.read())


def main():
    """
    Connect to google drive API and download the .csv files in storage
    :return: None
    """
    service = authenticate()
    download(service)


if __name__ == "__main__":
    main()
