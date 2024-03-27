from fondant.component import DaskLoadComponent
import dask.dataframe as dd
import pandas as pd
import requests
from bs4 import BeautifulSoup

class FetchLinks(DaskLoadComponent):
    def __init__(self, num_pages: int):
        self.pages = num_pages
    
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
        articles = soup.find_all('article', class_='card card--document')

        article = articles[0]
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

        response = requests.get(download_href)
        soup = BeautifulSoup(response.text, 'html.parser')
        speeches = soup.find_all('div', class_="meeting-speech")

        # Iterate over each speech div
        for speech in speeches:
            # Extract title
            title_div = speech.find("div", class_="meeting-speech__title")
            
            if title_div:
                reference = title_div.find('a')
                if reference:
                    profile = reference['href']
                else:
                    profile = ""
                title = title_div.text
            else:
                profile, title = "", ""
            
            text = ""
            spans = speech.find_all("span")
            
            for span in spans:
                text += " " + span.text
            
            data.append({
                'File Name': file_name,
                'Card title': card_title, 
                'Document number': doc_number, 
                'Download link href': download_href,
                'Profile': profile,
                'Title': title,
                'Text': text
                })

        return data