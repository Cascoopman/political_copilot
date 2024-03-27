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

        request_URL = f'https://www.vlaamsparlement.be/ajax/document-overview?page={page_number}&period=current_year_of_office&current_year_of_office_value=2022-2023&aggregaat%5B%5D=Vraag%20of%20interpellatie&aggregaattype%5B%5D=Schriftelijke%20vraag'

        headers = {'Accept': 'application/json'}
        response = requests.get(request_URL, headers=headers)

        json_content = response.json()
        html_content = json_content['html']

        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all articles with class "card card--document"
        articles = soup.find_all('article', class_='card card--document')
        i = 0
        # Loop through each article
        for article in articles:
            i += 1 
            # Extract the card title
            card_title = article.find('h3', class_='card__title').get_text()
            
            # Extract the document number
            doc_number = article.find('span', class_='card__document-number').get_text()
            
            # Find the link with class "card__link card__link-view"
            view_link = article.find('li', class_='card__link card__link-view')
            # Find the link with class "card__link card__link-download"
            download_link = article.find('li', class_='card__link card__link-download')
            
            # Extract the text and href attribute from the view link, if it exists        
            if view_link:
                view_text = view_link.get_text()
                view_href = view_link.find('a')['href']
            else:
                view_text, view_href = '', ''
            
            # Extract the text and href attribute from the download link, if it exists
            if download_link:
                download_text = download_link.get_text()
                download_href = download_link.find('a')['href']
            else:
                download_text, download_href = '', ''

            # add to dataframe
            card_title = card_title.replace("/", "_") #otherwise it will try to find a folder
            file_name = f"{card_title}_{doc_number}"
            data.append({
                'File Name': file_name,
                'Card title': card_title, 
                'Document number': doc_number, 
                'View link text': view_text,
                'View link href': view_href, 
                'Download link text': download_text, 
                'Download link href': download_href
                })

        return data