import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def is_valid_url(href):
    return href and not href.startswith("#") and not href.lower().startswith("javascript:")

def check_broken_links(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)

        print(f"\n🔍 Scanning {len(links)} links on: {url}\n")

        broken_links = []

        for tag in links:
            href = tag.get("href")
            if not is_valid_url(href):
                continue

            full_url = urljoin(url, href)
            try:
                r = requests.head(full_url, allow_redirects=True, timeout=5)
                if r.status_code == 404:
                    print(f"❌ Broken: {full_url} [404 Not Found]")
                    broken_links.append(full_url)
            except requests.RequestException:
                print(f"⚠️ Could not reach: {full_url}")
                broken_links.append(full_url)

        if not broken_links:
            print("\n✅ No broken links found!")
        else:
            print(f"\n🚨 Found {len(broken_links)} broken link(s):")
            for link in broken_links:
                print(link)

    except Exception as e:
        print(f"❌ Error fetching the page: {e}")

if __name__ == "__main__":
    url = input("Enter the URL (include https://): ").strip()
    check_broken_links(url)
