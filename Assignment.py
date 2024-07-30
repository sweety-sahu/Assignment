import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL
base_url = "https://hprera.nic.in/PublicDashboard"

# Send a GET request to the main page
response = requests.get(base_url)
response.raise_for_status()  # Raise an error for bad status codes

# Parse the main page content
soup = BeautifulSoup(response.text, 'html.parser')

# Find the links for the first 6 registered projects
project_links = soup.find_all('a', href=True, text='View Details')[:6]

project_details = []

# Loop through each project link
for link in project_links:
    project_url = "https://hprera.nic.in" + link['href']
    project_response = requests.get(project_url)
    project_response.raise_for_status()
    
    # Parse the project detail page
    project_soup = BeautifulSoup(project_response.text, 'html.parser')
    
    # Extract the required details
    details = {}
    details['GSTIN No'] = project_soup.find('td', text='GSTIN No').find_next_sibling('td').text.strip()
    details['PAN No'] = project_soup.find('td', text='PAN No').find_next_sibling('td').text.strip()
    details['Name'] = project_soup.find('td', text='Name').find_next_sibling('td').text.strip()
    details['Permanent Address'] = project_soup.find('td', text='Permanent Address').find_next_sibling('td').text.strip()
    
    project_details.append(details)

# Create a DataFrame and save to a CSV file
df = pd.DataFrame(project_details)
df.to_csv('project_details.csv', index=False)

print(df)
