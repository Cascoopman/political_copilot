from pathlib import Path
from fondant.pipeline import Pipeline
import os

BASE_PATH = "./fondant-artifacts"
Path(BASE_PATH).mkdir(parents=True, exist_ok=True)

GCP_PROJECT_NAME = os.getenv("GCP_PROJECT_NAME")

pipeline = Pipeline(
    name="pv_scraper",
    base_path=BASE_PATH,
)
# STEP 1: FETCH THE PDF DOWNLOAD LINKS
# Num pages set to 10 for demo purposes
# Manually check
links = pipeline.read(
    "components/scraper_components/fetchlinks_pv_component",
    arguments={
        "num_pages": 10,
    }
)

# STEP 2: DOWNLOAD THE CONTENT OF THE PDFS USING THE LINKS
raw_data = links.apply(
    "components/scraper_components/extract_pdf_text_component",
)

# STEP 3: EXTRACT AND STRUCTURE THE TEXT USING REGEX
regex_data = raw_data.apply(
    "components/scraper_components/regex_pv_component",
)

# STEP 4: STORE THE DATA IN A GCP BUCKET
regex_data.write(
    "write_to_file",
    arguments={
        "path": "gs://{GCP_PROJECT_NAME}_scrape/pv",
        "format": "parquet",
    }
)