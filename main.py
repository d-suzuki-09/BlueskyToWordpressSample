from atproto import Client
from datetime import datetime, timedelta
import requests

# Blueskyの1日前のポストを取得し、WordPressに投稿するスクリプト

# Blueskyの設定
# クライアントの作成
client = Client(base_url='https://bsky.social')
actorValue='did:xxxx'
limitValue=30
userName='xxxx.bsky.social'
# ログイン
client.login(login='xxxx.bsky.social',password='xxxx')

# 何日前のポストを取得するか
# 1日前のポストを取得する場合は1
timedeltaValue = 1

# WordPressのURL
MY_URL = "https://xxxx"
headers = {'Authorization': 'Basic xxxx'}


# 自分のタイムラインを取得
timeline = client.get_timeline()

# タイムラインからポストを抽出
data = client.get_author_feed(
    actor=actorValue,
    filter='posts',
    limit=limitValue,
)

posts = [post for post in data.feed]
output = ""

# postsの内容をテキストファイルに保存
# ファイルが存在する場合は上書き
# ファイルが存在しない場合は新規作成
# ファイル名は「posts_(今の時間).txt」
with open(f'posts_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt', 'w', encoding='UTF-8') as f:
    for post in posts:
        postString = str(post)
        if postString.find(userName) != -1 and postString.find((datetime.now()-timedelta(timedeltaValue)).strftime('%Y-%m-%d')) != -1:
            # f.write(postString + '\n')
            # postString の中の「text=」から次の「,」までを取得
            postText = postString[postString.find('text=') + 5:postString.find(',', postString.find('text='))]
            f.write(postText + '\n')
            print(postText)
            output = postText.replace('\'', '') + '\n\n' + output

# 出力内容確認
print(output)

# WordPressに投稿
post = {
            'title': '',
            'status': 'draft',
            'content': output,
        }
res = requests.post(f"{MY_URL}/wp-json/wp/v2/posts/", headers=headers, json=post)

# 結果確認
if res.ok:
    print(f"投稿の追加 成功 code:{res.status_code}")
else:
    print(f"投稿の追加 失敗 code:{res.status_code} reason:{res.reason} msg:{res.text}")
    
