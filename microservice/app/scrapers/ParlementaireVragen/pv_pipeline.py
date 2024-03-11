from pathlib import Path
from fondant.pipeline import Pipeline

BASE_PATH = "./fondant-artifacts"
Path(BASE_PATH).mkdir(parents=True, exist_ok=True)

pipeline = Pipeline(
    name="parlementaire-vragen",
    description="Retrieve pdf download links, download content, structure the content and index into vector DB.",
    base_path=BASE_PATH,
)

# Currently using reusable component, but will be replaced by a custom component
#from fetch_links import CreateLinks
raw_data = pipeline.read(
    "load_from_pdf",
    arguments={
        "pdf_path": "/output_pdfs/natuur_en_milieu",
    }
)

# Use the reusable component to structure the text
clean_data = raw_data.apply(
    "parlementaire_vragen_structure_text",
)

# OR: Use the lightweight component to structure the data
#from lw_structure_text import StructureText
#clean_data = raw_data.apply(
#    StructureText,
#)