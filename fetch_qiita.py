import os
import requests

QIITA_TOKEN = os.environ.get("QIITA_TOKEN")
USER_NAME = "TLyticsInsight"  # Qiitaのユーザー名を入力

url = f"https://qiita.com/api/v2/users/{USER_NAME}/items"
headers = {
    "Authorization": f"Bearer {QIITA_TOKEN}"
}

response = requests.get(url, headers=headers)
articles = response.json()

with open("qiita_articles.md", "w", encoding="utf-8") as f:
    f.write("# Qiita新着記事一覧\n\n")
    f.write("以下はQiitaに投稿した最新の記事です。\n\n")
for article in articles['data'][:10]:  # 最新10件表示（4件しかない場合でも問題なし）
    # 処理内容

        f.write(f"- [{article['title']}]({article['url']})\n")
    f.write("\n定期的に更新しています。\n")
