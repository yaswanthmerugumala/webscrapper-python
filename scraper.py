import requests
from bs4 import BeautifulSoup
import time
import random
import logging
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return None

def extract_paragraphs(soup):
    paragraphs = []
    for p in soup.find_all('p'):
        try:
            paragraphs.append(p.text.strip())
        except AttributeError:
            logging.warning("Error parsing paragraph text")
    return paragraphs

def extract_links(soup, base_url, keyword=None):
    links = []
    for link in soup.find_all('a', href=True):
        full_url = urljoin(base_url, link['href'])
        if not keyword or keyword in full_url:
            links.append(full_url)
    return links

def scrape_data(url):
    start_time = time.time()
    soup = get_soup(url)
    if not soup:
        return

    # Extract and print title
    title = soup.title.text.strip() if soup.title else 'No title found'
    print(f"Title of the webpage: {title}")

    # Extract and print paragraphs
    print("\nParagraphs:")
    paragraphs = extract_paragraphs(soup)
    for paragraph in paragraphs:
        print(paragraph)

    # Extract and print links
    print("\nLinks:")
    links = extract_links(soup, url)
    for link in links:
        print(link)

    duration = time.time() - start_time
    logging.info(f"Scraped data from {url} in {duration:.2f} seconds")

# Main function to run the scraper
if __name__ == "__main__":
    url = 'https://www.geeksforgeeks.org/python-web-scraping-tutorial/'
    scrape_data(url)
