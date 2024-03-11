import pyarrow as pa
import pandas as pd
from fondant.component import PandasTransformComponent
from fondant.pipeline import lightweight_component
import re

@lightweight_component(consumes={"text": pa.string()}, 
                       produces={"sender": pa.string(),
                                 "responder": pa.string(),
                                 "questions": pa.string(),
                                 "answers": pa.string(),
                                 "jurisdiction": pa.string(),
                                 "topic": pa.string(),
                                 "date": pa.string(),
                                 "number": pa.string()})
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
        dataframe['responder'] = dataframe['extracted_qa'].apply(lambda x: x['responder'])
        dataframe['questions'] = dataframe['extracted_qa'].apply(lambda x: x['questions'])
        dataframe['answers'] = dataframe['extracted_qa'].apply(lambda x: x['answers'])
        dataframe['jurisdiction'] = dataframe['extracted_qa'].apply(lambda x: x['jurisdiction'])
        dataframe['topic'] = dataframe['extracted_qa'].apply(lambda x: x['topic'])
        dataframe['date'] = dataframe['extracted_qa'].apply(lambda x: x['date'])
        dataframe['number'] = dataframe['extracted_qa'].apply(lambda x: x['number'])
        
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
            - sender: The sender of the message.
            - responder: The responder of the message.
            - questions: The questions asked in the message.
            - answers: The answers to the questions.
            - jurisdiction: The jurisdiction of the message.
            - topic: The topic of the message.
            - date: The date of the message.
            - number: The number of the message.
        """     
        # Define patterns to match            
        pattern = r'''(?s)SCHRIFTELIJKE VRAAG\n(?P<number>.+?)\nvan\s+(?P<sender>.+?)\ndatum:\s+(?P<date>.+)\naan\s+(?P<responder>.+?)\s*\n(?P<jurisdiction>.+?)\n(?P<topic>.+?)\n(?P<questions>.+)\n\s*(?P=responder)\s*\n(?P=jurisdiction)\s*\nANTWOORD\nop vraag\s*(?P=number)\s*van\s*(?P=date)\s*\nvan\s*(?P=sender)\s*\n(?P<answers>.+)$'''
        
        # Find matches for each pattern
        match = re.search(pattern, message)
        
        # If no match is found, return None
        if not match:
            print(f"Failed to match pattern for message: {message}")
            return {
                "number": None,
                "sender": None,
                "date": None,
                "responder": None,
                "jurisdiction": None,
                "topic": None,
                "questions": None,
                "answers": None
            }
        
        # Extract the data from the match, ensuring that the group exists
        number = None
        if match.group('number'):
            number = match.group('number')
        
        sender = None
        if match.group('sender'):
            sender = match.group('sender')
        
        date = None
        if match.group('date'):
            date = match.group('date')
            
        responder = None
        if match.group('responder'):
            responder = match.group('responder')
            
        jurisdiction = None
        if match.group('jurisdiction'):
            jurisdiction = match.group('jurisdiction')
        
        topic = None
        if match.group('topic'):
            topic = match.group('topic')
            
        questions = None
        if match.group('questions'):
            questions = match.group('questions')
            
        answers = None
        if match.group('answers'):
            answers = match.group('answers')
        
        # Return the extracted data        
        return {
            "number": number,
            "sender": sender,
            "date": date,
            "responder": responder,
            "jurisdiction": jurisdiction,
            "topic": topic,
            "questions": questions,
            "answers": answers
        }