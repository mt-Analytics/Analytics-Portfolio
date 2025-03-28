import os
import requests
import time

QIITA_TOKEN = os.environ.get("QIITA_TOKEN")
USER_NAME = "TLyticsInsight"  # Qiitaのユーザー名を入力

# ★ ここでトークンの長さを確認（デバッグ用）
print(f"Token length: {len(QIITA_TOKEN) if QIITA_TOKEN else 'Not Found'}")

url = f"https://qiita.com/api/v2/users/{USER_NAME}/items"
headers = {
    "Authorization": f"Bearer {QIITA_TOKEN}"
}

# API呼び出しにリトライ処理を追加
def fetch_with_retry(url, headers, retries=3, delay=5):
    for i in range(retries):
        response = requests.get(url, headers=headers)
        
        # ★ レスポンスの詳細を出力（デバッグ用）
        print("Attempt:", i+1)
        print("Status Code:", response.status_code)
        print("Response Headers:", response.headers)
        
        if response.status_code == 200:
            return response
        print(f"Attempt {i+1} failed. Retrying in {delay} seconds...")
        time.sleep(delay)
    
    print("全ての試行に失敗しました。")
    exit(1)

# APIリクエスト実行（リトライ付き）
response = fetch_with_retry(url, headers)

# レート制限チェック（修正後）
remaining_requests = response.headers.get("X-RateLimit-Remaining", "999")  # デフォルト値を 999 にする
print(f"Rate-Limit-Remaining: {remaining_requests}")  # デバッグ用に出力

try:
    remaining_requests = int(remaining_requests)
except ValueError:
    print(f"Warning: X-RateLimit-Remaining の値が予期しない形式: {remaining_requests}")
    remaining_requests = 999  # 安全策として999をセット

if remaining_requests == 0:
    print("APIのレート制限に達しました。しばらく待ってから再試行してください。")
    exit(1)

# ステータスコードチェック
if response.status_code != 200:
    print(f"Error: {response.status_code}, {response.json()}")
    exit(1)

# JSON解析とエラーハンドリング
try:
    articles = response.json()
    if not isinstance(articles, list):
        print("APIレスポンスが予期しない形式です:", articles)
        exit(1)
    if len(articles) == 0:
        print("記事が見つかりません。")
        exit(0)
except Exception as e:
    print("JSON解析中にエラーが発生しました:", str(e))
    exit(1)

# ファイル書き込み
with open("qiita_articles.md", "w", encoding="utf-8") as f:
    f.write("# Qiita新着記事一覧\n\n")
    f.write("以下はQiitaに投稿した最新の記事です。\n\n")

    for article in articles[:10]:  # 最新10件表示
        f.write(f"- [{article['title']}]({article['url']})\n")