Use this code to generate ironic and sarcastic tweets as if written by a political party representative.

### Dependencies
 - chromadb = "^0.4.21"
 - numpy = "^1.26.2"
 - openai = "^1.6.1"
 - sentence-transformers = "^2.2.2"
 - langchain = "^0.1.0"
 - ray = {extras = ["data"], version = "^2.9.0"}
 - python-dotenv = "^1.0.1"



### Steps
#### 1. Populate your vector database
Use `populate_vector_db.py` for this. Set the correct DATA folder; in this folder put the outputs of your party scrapers as separate files, e.g. vooruit.json, nva.json, etc.
The script will populate a local ChromaDB vector database, on disk.
This can take a while; but you only have to do it once.
In the ChromaDB vector database, a separate collection is created for each party.

#### 2. Generate tweet
Use `generate_tweet.py` for this. Create a .env file in which you put the following:
```
OPENAPI_KEY=<Paste OpenAI key here>
DATA_FOLDER=<Path to data folder>
CHUNK_SIZE=1500
CHUNK_OVERLAP=100

EMBEDDING_MODEL=distiluse-base-multilingual-cased-v2
CHROMA_PATH=<Path to chromadb database folder>
BATCH_SIZE=2048

TOKENIZERS_PARALLELISM=false
```

Arguments:
 - `--newsfile` a small txt file used as input. This file contains a news message to which the fake politician will react.
 - `--party` name of the party for which to generate a tweet
 - `--n` number of tweets to generate

For the party names, use the lowercase equivalents according to the following convention:
```
PARTIES = {
    'nva': 'N-VA',
    'cdv': 'CD&V',
    'vooruit': 'Vooruit',
    'vlaamsbelang': 'Vlaams Belang',
    'openvld': 'Open VLD',
    'pvda': 'PVDA',
    'groen': 'Groen',
}
```
