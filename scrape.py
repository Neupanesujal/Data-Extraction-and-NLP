import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Read the Excel file
file_path = '/home/sujal-neupane/drives/HDD/part1/BlackCoffer/Input.xlsx'  # Replace with the path to your .xlsx file
df = pd.read_excel(file_path)

# Create a folder to store all scraped content
output_folder = 'scraped_data'
os.makedirs(output_folder, exist_ok=True)

# Create a function to scrape a URL and save content to a text file
def scrape_and_save(url_id, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all instances of the specified class
    class_name = 'wp-block-heading'
    content = ""

    for tag in soup.find_all(class_=class_name):
        content += tag.get_text(strip=True) + '\n\n'

        # Extract paragraphs and list items following the tag
        sibling = tag.find_next_sibling()
        while sibling and sibling.name in ['p', 'ul', 'ol']:
            if sibling.name == 'p':
                content += sibling.get_text(strip=True) + '\n'
            elif sibling.name in ['ul', 'ol']:
                for li in sibling.find_all('li'):
                    content += f"- {li.get_text(strip=True)}\n"
            sibling = sibling.find_next_sibling()

        content += '\n'

    # Save the content to a text file named after the URL_ID
    file_path = os.path.join(output_folder, f'{url_id}.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"Scraping complete for URL_ID {url_id}. Content saved to {file_path}")

# Iterate through each URL in the DataFrame
for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    scrape_and_save(url_id, url)
