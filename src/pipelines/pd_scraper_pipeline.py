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

speeches.write(ref="write_to_file", arguments={"path": "gs://GCPPROJECTNAME _scrape/pv"})


#print(f"{GCP_PROJECT_NAME}"+"_scrape/pv")
#
# STEP 4: STORE THE DATA IN A GCP BUCKET
#regex_data.write(
#    "write_to_file",
#    arguments={
#        "path": f"gs://{GCP_PROJECT_NAME}_scrape/pv",
#        "format": "parquet",
#    }
#)