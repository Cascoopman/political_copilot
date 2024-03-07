from pathlib import Path
import pyarrow as pa
from fondant.pipeline import Pipeline
from fondant.pipeline.runner import DockerRunner

BASE_PATH = "./fondant-artifacts"

Path(BASE_PATH).mkdir(parents=True, exist_ok=True)

pipeline = Pipeline(
    name="parlementaire-vragen",
    description="Download the pdfs into a database and then index and vectorize them.",
    base_path=BASE_PATH,
)

from fetch_links import CreateLinks
raw_data = pipeline.read(
    ref=CreateLinks,
)