import os
import requests

def fetch_qiita_articles():
    token = os.environ.get('QIITA_TOKEN')
    if not token:
        print("Qiita token not found.")
        return

    url = 'https://qiita.com/api/v2/authenticated_user/items?page=1&per_page=100'
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch articles: {response.status_code}")
        print(response.text)
        return

    articles = response.json()

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write("# Qiita Articles\n\n")
        for article in articles:
            f.write(f"- [{article['title']}]({article['url']})\n")
    print("Successfully updated README.md")

if __name__ == "__main__":
    fetch_qiita_articles()
