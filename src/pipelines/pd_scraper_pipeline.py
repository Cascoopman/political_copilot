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
        "num_pages": 1,
    }
)

# STEP 3: CHUNK THE TEXT
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

# STEP 4: EMBED THE TEXT
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
