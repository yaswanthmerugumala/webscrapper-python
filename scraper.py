import requests
from bs4 import BeautifulSoup

# Function to scrape data
def scrape_website(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Example 1: Extracting the title of the webpage
            title = soup.title.text.strip()
            print(f"Title of the webpage: {title}")
            
            # Example 2: Extracting all paragraph texts
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                print(paragraph.text.strip())
            
            # Example 3: Extracting all links
            links = soup.find_all('a', href=True)
            print("\nLinks:")
            for link in links:
                print(link['href'])
            
        else:
            print(f"Failed to retrieve webpage. Status code: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching webpage: {e}")

# Main function to run the scraper
if __name__ == "__main__":
    url = 'https://www.geeksforgeeks.org/python-web-scraping-tutorial/'  # Replace with the URL you want to scrape
    scrape_website(url)
