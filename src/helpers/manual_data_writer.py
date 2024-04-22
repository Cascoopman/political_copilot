import os
import pandas as pd
import pyarrow as pa
import typing as t
import pyarrow.parquet as pq
import json
import itertools
from google.cloud import storage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings

# Define the schema
schema = pa.schema([
    ("id", pa.string()),
    ("text", pa.string()),
    ("faction", pa.string()),
    ("card_title", pa.string()),
    ("download_href", pa.string()),
    ("name", pa.string()),
    ("embedding", pa.list_(pa.float32()))
])

Path_to_parquet = "/Users/cas/Documents/political_agents/src/pipelines/fondant-artifacts/pd_scraper/pd_scraper-20240417151652/pd_speech_extractor_component/part.0.parquet"
table = pq.read_table(Path_to_parquet)

# Convert the Parquet table to a pandas DataFrame
df = table.to_pandas()

# Display the DataFrame
print(df.head())

def chunk_text(row) -> t.List[t.Tuple]:
    # Multi-index df has id under the name attribute
    doc_id = row.name
    text_data = row["text"]
    card_title = row["card_title"]
    download_href = row["download_href"]
    profile_href = row["profile_href"]
    name = row["name"]
    faction = row["faction"]
    
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=512,
        chunk_overlap=32,
        length_function=len,
        is_separator_regex=False,
    )
    docs = text_splitter.create_documents(texts=[text_data])

    return [
        (doc_id, f"{doc_id}_{chunk_id}", chunk.page_content, card_title, download_href, profile_href, name, faction)
        for chunk_id, chunk in enumerate(docs)
    ]
        
results = df.apply(
            chunk_text,
            axis=1,
        ).to_list()

# Flatten results
results = list(itertools.chain.from_iterable(results))

# Turn into dataframes
results_df = pd.DataFrame(
    results,
    columns=["original_document_id", "doc_id", "text", "card_title", "download_href", "profile_href", "name", "faction"],
)

print(results_df)

results_df.to_parquet('/Users/cas/Documents/political_agents/data/chunked.parquet')

embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small",)

def get_embeddings_vectors(texts):
    return embeddings_model.embed_documents(texts.tolist())

results_df["embedding"] = get_embeddings_vectors(
            results_df["text"],
        )
print(results_df)

results_df.to_parquet('/Users/cas/Documents/political_agents/data/embedded.parquet')

import json
import pandas as pd

path = '/Users/cas/Documents/political_agents/data/embedded.parquet'

df = pd.read_parquet(path)

print(df)

def create_json_records(df):
    json_records = []
    for index, row in df.iterrows():
        
        # Create JSON record
        record = {
            "id": row["doc_id"],
            "embedding": row["embedding"],
            "restricts": [
                    {
                        "namespace": "faction",
                        "allow": [row["faction"]]
                    },{
                        "namespace": "source",
                        "allow": ["PD"],
                    }
                ],
        }
        json_records.append(record)
    
    return json_records

def create_json_file(json_records, json_file_path):
    with open(json_file_path, 'w', encoding='utf-8') as f:
        for record in json_records:
            json.dump(record, f)
            f.write('\n')

json_path = "/Users/cas/Documents/political_agents/data"

df['embedding'] = df['embedding'].apply(lambda x: x.tolist())

json_records = create_json_records(df)

json_file = create_json_file(json_records, f"{json_path}"+"/final.json")