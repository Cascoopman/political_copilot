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
# Use a custom reusable (container) component to fetch the links
# Todo: make lightweight component into a container
# OR: Directly use a custom lightweight component to fetch the links

links = pipeline.read(
    "components/scraper_components/fetchlinks_pv_component",
    arguments={
        "link": 'https://www.vlaamsparlement.be/ajax/document-overview?page=0&period=current_year_of_office&current_year_of_office_value=2022-2023&aggregaat%5B%5D=Vraag%20of%20interpellatie&aggregaattype%5B%5D=Schriftelijke%20vraag',
        "num_pages": 1,
    }
)

# STEP 2: DOWNLOAD THE CONTENT OF THE PDFS USING THE LINKS
# Use the reusable component to load the remote pdfs
raw_data = links.apply(
    "components/scraper_components/extract_pdf_text_component",
)

# STEP 3: EXTRACT AND STRUCTURE THE TEXT USING REGEX
# Use the reusable component to structure the text (container: https://hub.docker.com/repository/docker/cascoopman/parlementaire_vragen_structure_text/general)
regex_data = raw_data.apply(
    "components/scraper_components/regex_pv_component",
)

print(f"{GCP_PROJECT_NAME}"+"_scrape/pv")

# STEP 4: STORE THE DATA IN A GCP BUCKET
regex_data.write(
    "write_to_file",
    arguments={
        "path": f"gs://{GCP_PROJECT_NAME}_scrape/pv",
        "format": "parquet",
    }
)