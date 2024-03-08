import pyarrow as pa
import pandas as pd
from fondant.component import PandasTransformComponent
from fondant.pipeline import lightweight_component
import re

@lightweight_component(consumes={"text": pa.string()}, 
                       produces={"sender": pa.string()})
class StructureText(PandasTransformComponent):  
    def transform(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Structure the original text into sender, responder, questions and the respective answer.

        Args:
            dataframe: A pandas DataFrame containing the text message.

        Returns:
            A pandas DataFrame with new columns for sender, responder, questions, and answers.
        """  

        # Assuming your text column name is 'text'
        dataframe['extracted_qa'] = dataframe['text'].apply(self.extract_qa)
        
        # Extracting data from the dictionary
        dataframe['sender'] = dataframe['extracted_qa'].apply(lambda x: x['sender'])
        
        # Drop the temporary column 'extracted_qa' if needed
        dataframe.drop('extracted_qa', axis=1, inplace=True)  # Uncomment to drop

        return dataframe

    @staticmethod
    def extract_qa(message):
        """Extracts the sender, the responder, and groups the questions with answers from the given message.

        Args:
            message: The message to extract the QA from.

        Returns:
            A dictionary with the following keys:
            * sender: The name of the sender.
            * responder: The name of the responder.
            * questions: A list of questions.
            * answers: A list of answers.
        """     
        print(message)
        # Define patterns to match            
        pattern_sender = r'''(?m)^SCHRIFTELIJKE VRAAG\n(?:.+\n)?^van\s+(?P<sender>.+)'''

        # Find matches for each pattern
        match_sender = re.search(pattern_sender, message)

        # Extract information from matches
        sender = match_sender.group('sender')
              
        return {
            "sender": sender,
        }