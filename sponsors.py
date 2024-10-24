import requests
from bs4 import BeautifulSoup
import sys

def fetch_sponsor_info(url):
    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all prize sections
    prizes = soup.find_all('div', class_='grid grid-cols-12 rounded-3xl pb-4 lg:p-4')

    if not prizes:
        print("No prizes found on the page.")
        return

    sponsors_info = []
    for prize in prizes:
        sponsor = {}
        sponsor['name'] = prize.find('h2').text.strip() if prize.find('h2') else 'N/A'
        sponsor['website'] = prize.find('a', href=True)['href'] if prize.find('a', href=True) else 'N/A'
        
        # Finding the 'docs' link if available
        docs_link = prize.find('a', href=True, text='Documentation')
        sponsor['docs_link'] = docs_link['href'] if docs_link else 'N/A'
        
        description_section = prize.find('div', class_='p-4 text-lg break-words whitespace-pre-line')
        sponsor['description'] = description_section.text.strip() if description_section else 'N/A'
        
        sponsors_info.append(sponsor)

    # Output the extracted information
    for sponsor in sponsors_info:
        print(f"Name: {sponsor['name']}")
        print(f"Website: {sponsor['website']}")
        print(f"Docs Link: {sponsor.get('docs_link', 'N/A')}")
        print(f"Description: {sponsor['description']}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fetch_sponsor_info.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    fetch_sponsor_info(url)