import dask.dataframe as dd
from fondant.component import DaskTransformComponent
import requests
import PyPDF2
from io import BytesIO


class ExtractText(DaskTransformComponent):
    def transform(self, dataframe: dd.DataFrame) -> dd.DataFrame:
        """Implement your custom logic in this single method
        Args:
            dataframe: A Pandas dataframe containing one partition of your data
        Returns:
            A pandas dataframe containing the transformed data
        """
        dataframe_with_text = dataframe.map_partitions(self.apply_extraction, meta={'text': 'string'})
        return dataframe_with_text
    
    @staticmethod
    def apply_extraction(partition):
        partition['text'] = partition['Download link href'].apply(ExtractText.extract)
        return partition[['text']]

    @staticmethod
    def extract(link):
        text = ""

        response = requests.get(link)
        if response.status_code == 200:
            pdf_content = BytesIO(response.content)
            pdf_reader = PyPDF2.PdfReader(pdf_content)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        else:
            print("Failed to fetch PDF:", response.status_code)

        return text