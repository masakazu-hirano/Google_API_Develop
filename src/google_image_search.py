from oauth_google import oauth_google

if __name__ == '__main__':
    search_client = oauth_google('image_search')

    response = search_client.cse().list(
        cx = '',   # ［必須］検索エンジンID
        gl = 'jp',
        cr = '日本',  # 検索結果を特定の国に限定する。
        hl = 'ja',  # インターフェース言語: ユーザーの入力言語と同じ言語で検索結果を表示する。
        siteSearch = '',  # 検索結果を指定したURLに限定する。
        q = '',  # 検索語句
        searchType = 'image',  # 項目値: 'web'，'image'
        imgColorType = 'color',
        # imgType = 'photo',  # 検索結果を指定したタイプに限定する。
        # imgDominantColor = '',  # 指定したメインカラーを持つ画像に限定する。
            # 項目値: 'red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'pink', 'white', 'gray', 'black', 'brown'
        safe = 'off'
    ).execute()

    print(response['items'])
