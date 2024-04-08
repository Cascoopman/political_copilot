from pathlib import Path
from fondant.pipeline import Pipeline
import os
import pyarrow as pa

BASE_PATH = "./fondant-artifacts"
Path(BASE_PATH).mkdir(parents=True, exist_ok=True)

GCP_PROJECT_NAME = os.getenv("GCP_PROJECT_NAME")

pipeline = Pipeline(
    name="pd_scraper",
    base_path=BASE_PATH,
)

# STEP 1: FETCH THE SPEECHES FROM DEBATES
# Use a custom reusable (container) component to fetch the speeches
speeches = pipeline.read(
    "components/scraper_components/pd_speech_extractor_component",
    arguments={
        "num_pages": 1,
    }
)

'''
# STEP 2: STORE THE DATA IN A GCP BUCKET
speeches.write(
    "write_to_file", 
    arguments={
        "path": "//pd"
    },
    consumes={
        "File Name": pa.string(),
        "Card title": pa.string(),
        "Document number": pa.string(),
        "Download link href": pa.string(),
        "Profile": pa.string(),
        "Faction": pa.string(),
        "Title": pa.string(),
        "Text": pa.string(),
    }
)
'''

chunked = speeches.apply(
    "components/scraper_components/pd_chunk_text",
    arguments={
        "chunk_strategy": "RecursiveCharacterTextSplitter",
        "chunk_kwargs": {
            "chunk_size": 512,
            "chunk_overlap": 40,
        },
    },
)

embedded = chunked.apply(
    "components/scraper_components/pd_embed_text",
    arguments={
        "model_provider": "openai",
        "model": "text-embedding-3-small",
        "api_keys": {
            "OPENAI_API_KEY": "//",
            },
        "auth_kwargs": {},
    },
)

embedded.apply(
    "components/scraper_components/pd_write_embeddings",
    arguments={
        "bucket_name": "//_embed",
        "json_file_name": "pd/embeddings.json",
    },
)