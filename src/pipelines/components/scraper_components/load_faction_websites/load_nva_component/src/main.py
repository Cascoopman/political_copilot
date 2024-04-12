#todo implement load component
import pandas as pd
import dask.dataframe as dd
from bs4 import BeautifulSoup  
import datetime
import requests
from fondant.component import DaskLoadComponent
from typing import  List
from dask.dataframe import from_pandas



class LoadNVA(DaskLoadComponent):

    def __init__(self) -> None:
        """
        Args:
            argumentX: An argument passed to the component
        """
        # Initialize your component here based on the arguments
        self.BASE_URL = 'https://www.n-va.be'

    def load(self) -> dd.DataFrame:
        
        data = ""
        try:
            response = requests.get(self.BASE_URL)
            response.raise_for_status()  # Raise an exception if the response status code is not 2xx
            data = response.json()

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")


        soup = BeautifulSoup(response.content, 'html.parser')
    
        # Find all links that start with /standpunten
        links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/standpunten/')]
        full_links = [self.BASE_URL + link for link in links]
        items = []

        # For each link, scrape the content of the div with ID 'content'
        for link in full_links:
            print(link)
            page_response = requests.get(link)
            page_soup = BeautifulSoup(page_response.content, 'html.parser')
            content_div = page_soup.find_all(class_='field--body')
            titles = page_soup.find_all(class_='page-title')
            subtitles = page_soup.find_all(class_='field--intro')
            
            # Save or process the content_div as needed
            if content_div:
                items.append({
                    'title': titles[0].text if titles else '',
                    'subtitle': subtitles[0].text if subtitles else '',
                    'content': content_div[0].text if content_div else '',
                    'uri': link
                })            

        return dd.from_pandas(pd.DataFrame(items), npartitions=1)