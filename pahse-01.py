import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor


def valid_filename(s):
    return "".join(c for c in s if c.isalnum() or c in ' .-').rstrip()

def fetch_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_title = valid_filename(soup.title.string.replace('/', '_'))
        with open(os.path.join('results', f'{page_title}.txt'), 'w', encoding='utf-8') as f:
            for paragraph in soup.find_all('p'):
                f.write(paragraph.text)
        print(f'Fetched: {url}')
        return soup
    except Exception as e:
        print(f'Error visiting {url}: {e}')

def crawl_wikipedia(seed_url, max_pages):
    pages_to_visit = [seed_url]
    visited_pages = set()
    page_count = 0

    # Create the results directory if it doesn't exist
    if not os.path.exists('results'):
        os.makedirs('results')

    with ThreadPoolExecutor(max_workers=10) as executor:
        while pages_to_visit and page_count < max_pages:
            url = pages_to_visit.pop(0)
            if url not in visited_pages:
                parsed_url = urlparse(url)
                if parsed_url.netloc == 'en.wikipedia.org':
                    soup = executor.submit(fetch_page, url).result()
                    if soup is not None:
                        visited_pages.add(url)
                        page_count += 1
                        for link in soup.find_all('a', href=True):
                            absolute_link = urljoin(url, link['href'])
                            if 'wikipedia.org' in absolute_link and absolute_link not in visited_pages:
                                pages_to_visit.append(absolute_link)

    print(f'Crawled {page_count} pages.')

crawl_wikipedia('https://en.wikipedia.org/wiki/Web_scraping', 100)


