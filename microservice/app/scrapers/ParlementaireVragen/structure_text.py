import pyarrow as pa
import pandas as pd
from fondant.component import PandasTransformComponent
from fondant.pipeline import lightweight_component
import regex

@lightweight_component(consumes={"text": pa.string()}, 
                       produces={"sender": pa.string(),
                                 "responder": pa.string(),
                                 "qna": pa.string()},
                       extra_requires=["regex"])
class StructureText(PandasTransformComponent):  
    def extract_qa(self, message):
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
        pattern = r'''(?m)^SCHRIFTELIJKE VRAAG nr. (?P<question_number>\d+) van (?P<questioner>.+) 
        datum: (?P<question_date>.+) aan (?P<minister>.+) VLAAMS MINISTER VAN (?P<minister_responsibilities>.+)
        (?P<question>.+)
        (?m)^ANTWOORD op vraag nr. (?P=question_number) van (?P=question_date) van (?P=questioner)
        (?P<answer>.+)
        '''

        for match in regex.finditer(pattern, message):
            sender = match.group('questioner')
            responder = match.group('minister')
            question = match.group('question'),
            answer = match.group('answer'),
            qna = f'''Questions from {sender}:\n{question}\nAnswers from {responder}:\n{answer}'''
        
        return {
            "sender": sender,
            "responder": responder,
            "qna": qna,
        }

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
        dataframe['qna'] = dataframe['extracted_qa'].apply(lambda x: x['qna'])
        
        # Drop the temporary column 'extracted_qa' if needed
        dataframe.drop('extracted_qa', axis=1, inplace=True)  # Uncomment to drop

        return dataframe
