import json
import re
import numpy as np
from pathlib import Path
import logging

import chromadb
from chromadb.utils import embedding_functions

from langchain.text_splitter import RecursiveCharacterTextSplitter

# Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
logging.basicConfig(level=logging.DEBUG)

# Create a logger
logger = logging.getLogger(__name__)


DATA_FOLDER = 'data/'
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 100

EMBEDDING_MODEL = 'distiluse-base-multilingual-cased-v2'
CHROMA_PATH = 'db/'
BATCH_SIZE = 2048


def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def create_json_dict(folder_path):
    json_dict = {}
    folder_path = Path(folder_path)

    for file_path in folder_path.glob('*.json'):
        filename = file_path.stem
        logger.info(filename)

        json_data = load_json_file(file_path)
        json_data_strip = [x['body'].strip() for x in json_data]
        json_dict[filename] = [x for x in json_data_strip if len(x) > 0]

    return json_dict

def chunk_docs(docs):
    text_splitter = RecursiveCharacterTextSplitter(
                separators=["\n\n", "\n", " ", ""],
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP,
                length_function=len
            )

    return text_splitter.create_documents(
                texts=[re.sub(r'\s+', ' ', x) for x in docs]
            )

def add_to_chroma_batched(docs, collection, partyname):
    number_of_batches = int(np.ceil(len(docs) / 2048))

    logging.info(f"Start to process {number_of_batches} batches for {partyname}")

    for i in range(number_of_batches):
        start_batch = i * BATCH_SIZE
        end_batch = (i + 1) * BATCH_SIZE

        collection.add(
            documents=[x.page_content for x in docs[start_batch:end_batch]],
            ids=[f"{partyname}_{i}" for i in range(start_batch, start_batch + len(docs[start_batch:end_batch]))]
        )

        logging.info(f"Added batch {i + 1}")
    logging.info(f"Done processing batches for {partyname}")


if __name__ == '__main__':
    partydocs = create_json_dict(DATA_FOLDER)
    for party in partydocs:
        partydocs[party] = chunk_docs(partydocs[party])

    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)

    for party in partydocs:
        collection = chroma_client.create_collection(
            name=party,
            embedding_function=embedding_function,
            metadata={"hnsw:space": "cosine"}
        )

        add_to_chroma_batched(
            docs=partydocs[party],
            collection=collection,
            partyname=party
        )
