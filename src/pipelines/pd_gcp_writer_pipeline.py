import os
import pandas as pd
import pyarrow as pa
import json
from google.cloud import storage

# Because of underlying issues with Fondant, we are unable to write the embeddings with it to a GCP bucket
# Thus: Manually using the latest parquet files created with Fondant
# to convert them to JSON and upload them to the GCP bucket

# Adjust variables to match the Fondant output
PARQUET_PARTS = 4
FONDANT_ARTIFACTS_PATH = "/Users/cas/Documents/political_agents/src/pipelines/fondant-artifacts/pd_scraper/pd_scraper-20240409075935"
scrape_bucket_name = "cedar-talent-417009_scrape"
embed_bucket_name = "cedar-talent-417009_embed"

# Define the schema
schema = pa.schema([
    ("id", pa.string()),
    ("faction", pa.string()),
    ("embedding", pa.list_(pa.float32()))
])

gcp_client = storage.Client()
scrape_bucket = gcp_client.get_bucket(scrape_bucket_name)
embed_bucket = gcp_client.get_bucket(embed_bucket_name)

def create_json_records(df):
    json_records = []
    for index, row in df.iterrows():
        
        # Create JSON record
        record = {
            "id": row["id"],
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
            json_string = json.dumps(record)
            f.write(json_string + '\n')
    
    with open(json_file_path, 'r', encoding='utf-8') as f:
        jsonl_content = f.read()
    
    return jsonl_content

# Upload the original docs, the chunks and the embeddings all in separate buckets 
for part in range(PARQUET_PARTS):
    json_file_name = f"pd_embeddings_part_{part}.json"
    PARQUET_EMBED_PATH = f"{FONDANT_ARTIFACTS_PATH}/pd_embed_text/part.{part}.parquet"

    df = pd.read_parquet(PARQUET_EMBED_PATH, engine='pyarrow', columns=['id', 'faction', 'embedding'], schema=schema)
    df['embedding'] = df['embedding'].apply(lambda x: x.tolist())

    json_records = create_json_records(df)

    output_file_path = 'tmp/'
    os.makedirs(output_file_path, exist_ok=True)
    json_file_path = os.path.join(output_file_path, json_file_name)

    json_file = create_json_file(json_records, json_file_path)

    embed_blob = embed_bucket.blob(json_file_name)

    #embed_blob.upload_from_string(json_file)
    
    PARQUET_CHUNK_PATH = f"{FONDANT_ARTIFACTS_PATH}/pd_chunk_text/part.{part}.parquet"
    chunk_file_path = os.path.join(FONDANT_ARTIFACTS_PATH, PARQUET_CHUNK_PATH)
    blob = scrape_bucket.blob(f"pd/chunks/part.{part}.parquet")
    blob.upload_from_filename(chunk_file_path)
    
PARQUET_ORIGINALDOC_PATH = f"{FONDANT_ARTIFACTS_PATH}/pd_speech_extractor_component/part.0.parquet"
chunk_file_path = os.path.join(FONDANT_ARTIFACTS_PATH, PARQUET_ORIGINALDOC_PATH)
blob = scrape_bucket.blob(f"pd/original_doc/part.0.parquet")
blob.upload_from_filename(chunk_file_path)