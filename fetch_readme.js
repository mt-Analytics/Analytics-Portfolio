async function fetchReadme() {
  const username = 'TLyticsInsight';
  const repo = 'Analytics-Portfolio';
  const url = `https://api.github.com/repos/${username}/${repo}/readme`;

  try {
    const response = await fetch(url, {
      headers: { Accept: 'application/vnd.github.v3+json' }
    });

    if (!response.ok) {
      throw new Error('READMEを取得できませんでした');
    }

    const data = await response.json();
    const readmeContent = decodeURIComponent(escape(atob(data.content)));

    // READMEの内容を表示
    document.getElementById('readme-container').innerHTML = marked.parse(readmeContent);
  } catch (error) {
    console.error('エラー:', error);
  }
}

document.addEventListener('DOMContentLoaded', fetchReadme);
