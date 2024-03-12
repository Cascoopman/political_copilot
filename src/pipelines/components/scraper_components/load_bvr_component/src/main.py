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
                news_items.append({
                    'id': item['id'],
                    'Type': item['type'],
                    'Title': item['attributes']['title']
                })

        return dd.from_pandas(pd.DataFrame(news_items), npartitions=1)
        

# class NewsItem:
#     def __init__(self, type, id, attributes,raw_json):
#         self.type = type
#         self.id = id
#         self.attributes = attributes
#         self.raw_json = raw_json

# class NewsAttributes:
#     def __init__(self, title, alternativeTitle, htmlContent, position, mandateeNames, mandateeFirstNames,
#                  mandateeFamilyNames, mandateeIds, mandateeTitles, meetingDate, meetingId, meetingTypePosition,
#                  themeId, agendaitemType, uuid, uri):
#         self.title = title
#         self.alternativeTitle = alternativeTitle
#         self.htmlContent = htmlContent
#         self.position = position
#         self.mandateeNames = mandateeNames
#         self.mandateeFirstNames = mandateeFirstNames
#         self.mandateeFamilyNames = mandateeFamilyNames
#         self.mandateeIds = mandateeIds
#         self.mandateeTitles = mandateeTitles
#         self.meetingDate = meetingDate
#         self.meetingId = meetingId
#         self.meetingTypePosition = meetingTypePosition
#         self.themeId = themeId
#         self.agendaitemType = agendaitemType
#         self.uuid = uuid
#         self.uri = uri
