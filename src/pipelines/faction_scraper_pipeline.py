from fondant.pipeline import Pipeline
from pathlib import Path


BASE_PATH = "./fondant-artifacts"
Path(BASE_PATH).mkdir(parents=True, exist_ok=True)

pipeline = Pipeline(
    name="faction_scraper",
    base_path=BASE_PATH
)

dataset = pipeline.read(
    "components/scraper_components/load_faction_websites/load_nva_component"
)


