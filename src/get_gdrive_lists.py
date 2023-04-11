from authenticate_google_oauth import auth_google

if __name__ == '__main__':
    gdrive_client = auth_google()
    files = []

    page_token = None
    while True:
        response = gdrive_client.files().list(
            corpora = 'user',
            spaces='drive',
            fields = 'files(id, mimeType, name), nextPageToken',
            q = "mimeType != 'application/vnd.google-apps.folder' and 'root' in parents",
                # https://developers.google.com/drive/api/guides/search-files#examples
            orderBy = 'folder, name, modifiedTime',
            pageSize = 1000,
            pageToken = page_token
        ).execute()

        print(response['files'])
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
