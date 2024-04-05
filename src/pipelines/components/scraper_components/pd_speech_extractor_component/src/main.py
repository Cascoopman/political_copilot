from fondant.component import DaskLoadComponent
import dask.dataframe as dd
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

class FetchLinks(DaskLoadComponent):
    def __init__(self, num_pages: int):
        self.pages = num_pages
        self.regering = {
            "jan-jambon": "N-VA",
            "ben-weyts": "N-VA",
            "zuhal-demir": "N-VA",
            "matthias-diependaele": "N-VA",
            "bart-somers": "Open Vld",
            "lydia-peeters": "Open Vld",
            "gwendolyn-rutten": "Open Vld",            
            "benjamin-dalle": "cd&v",
            "jo-brouns": "cd&v",
            "wouter-beke": "cd&v",
            "hilde-crevits": "cd&v",
        }
    
    def get_pages(self):
        return self.pages
    
    def load(self) -> dd.DataFrame:
        data = []

        for page_number in range(0, self.get_pages()):
            data.extend(self.fetch_document_info(page_number))

        df = pd.DataFrame(data)
        
        return dd.from_pandas(df, npartitions=1)
    
    def fetch_document_info(self, page_number):
        data = []

        link = f'https://www.vlaamsparlement.be/ajax/document-overview?page={page_number}&period=current_parliamentary_term&current_parliamentary_term_value=2019-2024&aggregaat%5B%5D=Actualiteitsdebat'
                                                                                        
        headers = {'Accept': 'application/json'}
        response = requests.get(link, headers=headers)

        json_content = response.json()
        html_content = json_content['html']

        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all articles with class "card card--document"
        # These are the cards that contain the links to all debates
        articles = soup.find_all('article', class_='card card--document')

        # Iterate over each article to extract the debate information
        for article in articles:
            card_title = article.find('h3', class_='card__title').get_text()
            download_link = article.find('li', class_='card__link card__link-download')
            doc_number = article.find('span', class_='card__document-number').get_text()

            # Extract the text and href attribute from the download link, if it exists
            if download_link:
                download_href = download_link.find('a')['href']
            else:
                download_href = ''

            card_title = card_title.replace("/", "_") #otherwise it will try to find a folder
            file_name = f"{card_title}_{doc_number}"

            # Fetch the content of the debate
            response = requests.get(download_href)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all divs with class "meeting-speech"
            # These are the blocks of debate text ordered per person
            speeches = soup.find_all('div', class_="meeting-speech")

            # Iterate over each speech div
            for speech in speeches:
                
                # Extract title
                title_div = speech.find("div", class_="meeting-speech__title")
                
                if title_div:
                    reference = title_div.find('a')
                    if reference:
                        profile = "https://www.vlaamsparlement.be"+reference['href']
                    else:
                        profile = ""
                    name = title_div.text
                else:
                    profile, name = "", ""
                
                # Drop De voorzitter and empty names
                if name == "De voorzitter" or name == "":
                    continue
                
                # Extract which faction the person belongs to
                pattern = r'\((.*?)\)'
                matches = re.search(pattern, name)
                if matches:
                    faction = matches.group(1)
                else:
                    faction = ""
                
                # If the faction is not found in the name, the person is part of the regering 2019-2024
                if faction == "" and profile == "":
                    name_parts = name.split(' ')[1:]
                    # Join the name parts with '-'
                    formatted_name = '-'.join(name_parts).lower()
                    profile = f"https://www.vlaanderen.be/vlaamse-regering/{formatted_name}"
                    try:
                        faction = self.regering[formatted_name]
                    except KeyError:
                        print(f"Could not find faction name for {name}, {download_href}")
                        faction = ""
                
                # Some outliers are not part of the regering but their name didn't contain a profile link yet 
                if profile == "":
                    name_parts = name.split(' ')[1:]
                    # Join the name parts with '-'
                    formatted_name = '-'.join(name_parts).lower()
                    profile = f"https://www.vlaamsparlement.be/nl/vlaamse-volksvertegenwoordigers-het-vlaams-parlement/{formatted_name}"

                # Some outliers were part of the regering 2019-2024 but did have a profile link in their name
                if faction == "":
                    name_parts = name.split(' ')[1:]
                    # Join the name parts with '-'
                    formatted_name = '-'.join(name_parts).lower()     
                    try:
                        faction = self.regering[formatted_name]
                    except KeyError:
                        print(f"Could not find faction name for {name}, {download_href}")
                        faction = ""
                
                # For each speech, extract the text grouped in paragraphs
                text = ""
                paragraphs = speech.find_all("p")
                
                # Some texts are further nested in a span tag, others are directly in the paragraph
                for paragraph in paragraphs:
                    if not paragraph.text:
                        span = paragraph.find("span")
                        text += " " + span.text
                    else:
                        text += " " + paragraph.text
                
                # Append to the database
                data.append({
                    'card_title': card_title, 
                    'download_href': download_href,
                    'profile_href': profile,
                    'faction': faction,
                    'name': name,
                    'text': text
                    })

        return data