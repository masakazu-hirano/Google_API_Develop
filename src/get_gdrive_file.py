import boto3
import io
import os

from botocore.config import Config
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

def oauth_google():
    scope = ['SCOPE']
    credential = None
    if os.path.exists('token.json'):
        credential = Credentials.from_authorized_user_file('token.json', scope)

    if not credential or not credential.valid:
        if credential and credential.expired and credential.refresh_token:
            credential.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scope)
            credential = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(credential.to_json())

    return build('drive', 'v3', credentials=credential)

def auth_cloudflare():
    return boto3.client('s3',
        endpoint_url = 'URL',
        aws_access_key_id = 'Access Key ID',
        aws_secret_access_key = 'Secret Access Key',
        config = Config(signature_version = 'v4')
    )

def gdrive_file_delete(file_id, file_name):
    gdrive_client.files().delete(fileId=file_id).execute()
    print(f'{file_name} は削除されました。')

if __name__ == '__main__':
    gdrive_client = oauth_google()

    page_token = None
    while True:
        response = gdrive_client.files().list(
            corpora = 'user',
            spaces='drive',
            fields = 'files(id, mimeType, name), nextPageToken',
            q = "検索クエリ",
                # https://developers.google.com/drive/api/guides/search-files#examples
            orderBy = 'folder, name, modifiedTime',
            pageSize = 1000,
            pageToken = page_token
        ).execute()

        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    gdrive_file_lists = []
    for gdrive_file in response['files']:
        gdrive_file_lists.append({
            'id': gdrive_file['id'],
            'name': gdrive_file['name']
        })

    for gdrive_file in gdrive_file_lists:
        gdrive_client.files().get(fileId=gdrive_file['id']).execute() # ファイル取得
        gdrive_file_delete(gdrive_file['id'], gdrive_file['name']).execute() # ファイル削除

        # ▼ バイナリファイル ダウンロード ▼
        download_file = io.BytesIO()
        MediaIoBaseDownload(
            download_file,
            gdrive_client.files().get_media(fileId = gdrive_file['id'])
        ).next_chunk()

        with open(f"download_file/{gdrive_file['name']}", 'xb') as file:
            file.write(download_file.getbuffer())
        # ▲ バイナリファイル ダウンロード ▲

    boto3_client = auth_cloudflare()
    boto3_client.upload_file('アップロードファイルパス', 'バケット名', 'キー名（ファイル名）')

    print('処理が正常終了しました。')
