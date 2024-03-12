import os
import argparse
import logging
import dotenv

import chromadb
from chromadb.utils import embedding_functions

#import openai
import ollama
#MODEL_NAME='mistral'
MODEL_NAME='llama2:7b-chat'

import prompts

# Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
logging.basicConfig(level=logging.DEBUG)

# Create a logger
logger = logging.getLogger(__name__)

# Reload the variables in your '.env' file (override the existing variables)
dotenv.load_dotenv(".env", override=True)

CHROMA_CLIENT = chromadb.PersistentClient(path=os.environ.get('CHROMA_PATH'))
EMBEDDING_FUNCTION = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=os.environ.get('EMBEDDING_MODEL')
)
#OPENAI_CLIENT = openai.OpenAI(
#    api_key=os.environ.get('OPENAPI_KEY')
#)

PARTIES = {
    'nva': 'N-VA',
    'cdv': 'CD&V',
    'vooruit': 'Vooruit',
    'vlaamsbelang': 'Vlaams Belang',
    'openvld': 'Open VLD',
    'pvda': 'PVDA',
    'groen': 'Groen',
}

POLITICIANS = {
    'nva': 'Bert De Waver',
    'cdv': 'Massy Mahdi',
    'vooruit': 'Selima De Praetere',
    'vlaamsbelang': 'Tim Van Grokken',
    'openvld': 'Tom Angeno',
    'pvda': 'Roland Hedebouw',
    'groen': 'Nija Nadia',
}

PROMPTS = {
    'nva': 'Je spreekt soms in Latijnse zegswijzen',
    'openvld': 'Je bent liberaal',
    'vooruit': 'Je bent progressief en socialistisch',
    'groen': 'Je bent progressief en klimaatbewust, heel soms woke',
    'vlaamsbelang': 'Je bent rechts, nationalistisch, soms populistisch',
    'pvda': 'Je bent progressief, marxistisch, soms populistisch',
    'cdv': 'Je bent centrumrechts en hangt katholieke waarden aan',
}


def read_file_into_string(newsfile: str) -> str:
    try:
        with open(newsfile, 'r') as file:
            file_contents = file.read()
        return file_contents
    except FileNotFoundError:
        logger.error(f"File '{newsfile}' not found.")
        return ''

""""
def get_openai_response(prompt: str) -> str:
    openai_completion = OPENAI_CLIENT.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4-1106-preview",
    )

    return openai_completion
"""

def clean_response_text(response: str) -> str:
    if response.endswith('"') and response.startswith('"'):
        return response[1:-1]
    return response


def run(newsfile: str, party: str, n: int):
    news_message = read_file_into_string(newsfile)
    if len(news_message) == 0:
        logger.info(f"Shutting down.")
        return
    
    available_collections = [c.name for c in CHROMA_CLIENT.list_collections()]
    if party not in available_collections:
        logger.error(f"Party {party} not found in vector database.")
        logger.info(f"Shutting down.")
        return
    
    collection = CHROMA_CLIENT.get_collection(
            name=party,
            embedding_function=EMBEDDING_FUNCTION,
        )
    
    query = news_message

    chroma_results = collection.query(
        query_texts=[query],
        n_results=150
    )

    chroma_contexts = '\n'.join(chroma_results['documents'][0])
    print(chroma_contexts)
    press_release_prompt = prompts.create_press_release_prompt(
        POLITICIANS[party], PARTIES[party], query, chroma_contexts
    )
    logger.info(f"\nWaiting...")
    
    # query OpenAI here
    """
    press_release_completion = get_openai_response(press_release_prompt)
    press_release = press_release_completion.choices[0].message.content
    """
    
    # query local LLM here
    press_release_completion = ollama.chat(model=MODEL_NAME, messages=[
        {
            'role': 'user',
            'content': press_release_prompt,
        }
    ])
    press_release = press_release_completion['message']['content']
    #print(press_release)
    logger.debug(f"Press release statement:\n{press_release}")
    
    twitter_prompt = prompts.create_twitter_prompt(
        POLITICIANS[party], PARTIES[party], PROMPTS[party], query, press_release
    )

    for iteration in range(n):
        logger.info(f"\nWaiting...")
        #tweet_completion = get_openai_response(twitter_prompt)
        #tweet = tweet_completion.choices[0].message.content
        tweet_completion = ollama.chat(model=MODEL_NAME, messages=[
        {
            'role': 'user',
            'content': twitter_prompt,
        }
        ])
        tweet = tweet_completion['message']['content']
        
        tweet = clean_response_text(tweet)
        
        logger.info(f"Tweet {iteration + 1}:\n{tweet}")
        print(f"Tweet {iteration + 1}:\n{tweet}")
        print(tweet)
    
    logger.info(f"\nDone.")


def main():
    parser = argparse.ArgumentParser(
        description='Generate n tweets by a party representative reacting to a news message'
    )
    parser.add_argument('--newsfile', type=str, help='Path to the news message file')
    parser.add_argument('--party', type=str, help='Political party')
    parser.add_argument('--n', type=int, help='Number of tweets to generate')

    args = parser.parse_args()

    newsfile = args.newsfile
    party = args.party
    n = args.n

    print("News File:", newsfile)
    print("Party:", party)
    print("N:", n)

    run(newsfile, party, n)

if __name__ == "__main__":
    main()
