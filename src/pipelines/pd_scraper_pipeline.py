from pathlib import Path
from fondant.pipeline import Pipeline
import os

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
        "num_pages": 10,
    }
)

# STEP 3: CHUNK THE DATA INTO SMALLER PARTS
#dataset = dataset.apply(
#    "chunk_text",
#    arguments={
        # Add arguments
        # "chunk_strategy": "RecursiveCharacterTextSplitter",
        # "chunk_kwargs": {},
        # "language_text_splitter": ,
#    },
#)

# STEP 4: GENERATE EMBEDDINGS
#dataset = dataset.apply(
#    "embed_text",
#    arguments={
        # Add arguments
        # "model_provider": "huggingface",
        # "model": ,
        # "api_keys": {},
        # "auth_kwargs": {},
#    },
#)

# STEP 5: STORE THE DATA IN A GCP BUCKET
#print(f"{GCP_PROJECT_NAME}"+"_scrape/pv")
speeches.write(
    "write_to_file", 
    arguments={
        "path": "gs://GCP_PROJECT_NAME_scrape/pd"
    }
)