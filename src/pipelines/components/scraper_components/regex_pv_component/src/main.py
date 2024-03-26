import dask.dataframe as dd
from fondant.component import DaskTransformComponent
import re

class StructureText(DaskTransformComponent):  
    def transform(self, dataframe: dd.DataFrame) -> dd.DataFrame:
        """Structure the original text into sender, responder, questions and the respective answer.

        Args:
            dataframe: A pandas DataFrame containing the text message.

        Returns:
            A pandas DataFrame with new columns for sender, responder, questions, and answers.
        """  

        dataframe_with_qa = dataframe.map_partitions(self.apply_extract_qa, 
                                                     meta={
                                                         'extracted_qa': 'string'})
        
        # Extract individual columns from the dictionary and assign them to new columns
        dataframe_with_columns = dataframe_with_qa.assign(
            number=dataframe_with_qa['extracted_qa'].apply(lambda x: x['number'], meta=('number', 'string')),
            sender=dataframe_with_qa['extracted_qa'].apply(lambda x: x['sender'], meta=('sender', 'string')),
            date=dataframe_with_qa['extracted_qa'].apply(lambda x: x['date'], meta=('date', 'string')),
            responder=dataframe_with_qa['extracted_qa'].apply(lambda x: x['responder'], meta=('responder', 'string')),
            jurisdiction=dataframe_with_qa['extracted_qa'].apply(lambda x: x['jurisdiction'], meta=('jurisdiction', 'string')),
            topic=dataframe_with_qa['extracted_qa'].apply(lambda x: x['topic'], meta=('topic', 'string')),
            questions=dataframe_with_qa['extracted_qa'].apply(lambda x: x['questions'], meta=('questions', 'string')),
            answers=dataframe_with_qa['extracted_qa'].apply(lambda x: x['answers'], meta=('answers', 'string'))
        )
        
        # Drop the temporary column 'extracted_qa'
        dataframe_with_columns = dataframe_with_columns.drop(columns='extracted_qa')
        
        return dataframe_with_columns

    @staticmethod
    def apply_extract_qa(partition):
        partition['extracted_qa'] = partition['text'].apply(StructureText.extract_qa)
        return partition[['extracted_qa']]
    
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
        header_pattern = r'''[\s\n]*SCHRIFTELIJKE VRAAG[\s\n]*(?P<number>.+?)[\s\n]*van[\s\n]*(?P<sender>.+?)[\s\n]*datum:[\s\n]*(?P<date>.+?)[\s\n]*aan[\s\n]*(?P<responder>.+?)[\s\n]*\n[\s\n]*(?P<jurisdiction>.+?)\s*\n\s*(?P<topic>.+?)\s*\n'''
        questions_pattern = r'''[\s\n]*SCHRIFTELIJKE VRAAG[\s\n]*(?P<number>.+?)[\s\n]*van[\s\n]*(?P<sender>.+?)[\s\n]*datum:[\s\n]*(?P<date>.+?)[\s\n]*aan[\s\n]*(?P<responder>.+?)[\s\n]*\n[\s\n]*(?P<jurisdiction>.+?)\s*\n\s*(?P<topic>.+?)\s*\n(?P<questions>[\s\S]*)(?P=responder)\s*\n\s*(?P=jurisdiction)\s*\n\s*ANTWOORD\s*'''
        answers_pattern = r'''[\s\n]*SCHRIFTELIJKE VRAAG[\s\n]*(?P<number>.+?)[\s\n]*van[\s\n]*(?P<sender>.+?)[\s\n]*datum:[\s\n]*(?P<date>.+?)[\s\n]*aan[\s\n]*(?P<responder>.+?)[\s\n]*\n[\s\n]*(?P<jurisdiction>.+?)\s*\n\s*(?P<topic>.+?)\s*\n(?P<questions>[\s\S]*)(?P=responder)\s*\n\s*(?P=jurisdiction)\s*\n\s*ANTWOORD[\s\S]*(?P=sender)(?P<answers>[\s\S]*)'''
          
        # Find matches for each pattern
        header_match = re.search(header_pattern, message)
        questions_match = re.search(questions_pattern, message)
        answers_match = re.search(answers_pattern, message)
        
        # If no match is found, return None
        if not header_match or not questions_match or not answers_match:
            print("Failed to match pattern for message: \n")
            print(repr(message))
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
        if header_match.group('number'):
            number = header_match.group('number')
        
        sender = None
        if header_match.group('sender'):
            sender = header_match.group('sender')
        
        date = None
        if header_match.group('date'):
            date = header_match.group('date')
            
        responder = None
        if header_match.group('responder'):
            responder = header_match.group('responder')
            
        jurisdiction = None
        if header_match.group('jurisdiction'):
            jurisdiction = header_match.group('jurisdiction')
        
        topic = None
        if header_match.group('topic'):
            topic = header_match.group('topic')
            
        questions = None
        if questions_match.group('questions'):
            questions = questions_match.group('questions')
            
        answers = None
        if answers_match.group('answers'):
            answers = answers_match.group('answers')
        
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