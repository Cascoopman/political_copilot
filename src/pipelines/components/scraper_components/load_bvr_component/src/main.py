#todo implement load component
import pandas as pd
import dask.dataframe as dd
import datetime
import requests
from fondant.component import DaskLoadComponent
from typing import  List
from dask.dataframe import from_pandas


class LoadBVR(DaskLoadComponent):

    def __init__(self) -> None:
        """
        Args:
            argumentX: An argument passed to the component
        """
        # Initialize your component here based on the arguments
        self.from_date = datetime.date.fromisoformat('2009-11-26')
        self.to_date = datetime.date.fromisoformat('2009-11-28')
        self.BASE_URL = 'https://beslissingenvlaamseregering.vlaanderen.be/news-items/search'

    def load(self) -> dd.DataFrame:
        
        data = ""
        try:
            params = {'page[size]': 5000,
                    'page[number]': 0,
                    'filter[:gte,lte:meetingDate]': str(self.from_date) + ',' + str(self.to_date)}
            
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()  # Raise an exception if the response status code is not 2xx
            data = response.json()

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

        news_items = []

        if data:
            for item in data['data']:
                print(item)
                news_items.append({
                    'id': item['id'],
                    'type': item['type'],
                    'title': item['attributes']['title'],
                    'position': item['attributes']['position'],
                    'htmlContent': item['attributes']['htmlContent'],
                    'meetingDate': item['attributes']['meetingDate'],
                    'mandateeNames': item['attributes']['mandateeFirstNames'] + ' ' + item['attributes']['mandateeFamilyNames'],
                    'mandateeTitles': ', '.join(item['attributes']['mandateeTitles']),
                    'htmlContent': item['attributes']['htmlContent'],
                    'uri': item['attributes']['uri']
                })

        return dd.from_pandas(pd.DataFrame(news_items), npartitions=1)