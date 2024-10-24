import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm
import pandas as pd
import time

def fetch_showcase_links(base_url, max_pages):
    all_links = []
    current_page = 1

    with tqdm(total=max_pages, desc="Fetching pages") as pbar:
        while current_page <= max_pages:
            url = f"{base_url}?page={current_page}"
            response = requests.get(url)
            
            if response.status_code != 200:
                print(f"Failed to fetch page {current_page}. Status code: {response.status_code}")
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            showcase_links = soup.find_all('a', href=lambda href: href and '/showcase/' in href and 'page=' not in href)
            
            if not showcase_links:
                print(f"No more showcase links found on page {current_page}. Stopping pagination.")
                break

            print(f"\nLinks fetched from page {current_page}:")
            for link in showcase_links:
                href = link.get('href')
                full_url = urljoin(base_url, href)
                if full_url not in all_links:
                    all_links.append(full_url)
                    print(full_url)

            pbar.update(1)
            current_page += 1

        print(f"\nTotal links fetched: {len(all_links)}")

    return all_links

def fetch_project_details(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Fetch GitHub link
        github_link = soup.find('a', href=lambda href: href and 'github.com' in href)
        github_url = github_link['href'] if github_link else ''
        
        # Fetch Project Description
        description_header = soup.find('h3', string='Project Description')
        description = ''
        if description_header:
            description = description_header.find_next('p').text.strip()
        
        # Fetch How it's Made
        how_its_made_header = soup.find('h3', string="How it's Made")
        how_its_made = ''
        if how_its_made_header:
            how_its_made = how_its_made_header.find_next('p').text.strip()
        
        return github_url, description, how_its_made
    else:
        print(f"Failed to fetch project details. Status code: {response.status_code}")
        return '', '', ''

# Example usage
base_url = "https://ethglobal.com/showcase"
max_pages = 30  # Change this to the desired number of pages

all_showcase_links = fetch_showcase_links(base_url, max_pages)

# Create a list to store all project data
project_data = []

# Fetch details for each project
for index, link in enumerate(all_showcase_links, 1):
    github_url, description, how_its_made = fetch_project_details(link)
    project_data.append({
        'URL': link,
        'Source Code': github_url,
        'Project Description': description,
        'How its Made': how_its_made
    })
    
    # Print details of every entry
    print(f"\nEntry {index}:")
    print(f"URL: {link}")
    print(f"Source Code: {github_url}")
    print(f"Project Description: {description[:100]}..." if len(description) > 100 else f"Project Description: {description}")
    print(f"How it's Made: {how_its_made[:100]}..." if len(how_its_made) > 100 else f"How it's Made: {how_its_made}")
    print("-" * 50)
    
    time.sleep(1)  # Add a delay to avoid overwhelming the server

# Create a DataFrame from the collected data
df = pd.DataFrame(project_data)

# Save the DataFrame to a CSV file
csv_filename = 'showcase_links_details.csv'
df.to_csv(csv_filename, index=False)

print(f"\nTotal projects found: {len(project_data)}")
print(f"Data saved to {csv_filename}")

# Display the first few rows of the DataFrame
print(df.head())
