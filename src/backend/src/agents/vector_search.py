import autogen
import os
from google.cloud import storage
from google.cloud import aiplatform
from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import Namespace
from openai import OpenAI
import pandas as pd

def vector_search(query: str, faction: str, topK = 10, source = "PD") -> list:
    # Define environment variables
    PROJECT_ID = os.environ.get('GCP_PROJECT_NAME')
    LOCATION = 'europe-west1'

    # Set variables for the current deployed index.
    INDEX_ENDPOINT= os.environ.get('GCP_INDEX_ENDPOINT')
    DEPLOYED_INDEX_ID="political_endpoint"
    
    current_directory = os.path.dirname(__file__)
    absolute_path = os.path.abspath(os.path.join(current_directory, "OAI_CONFIG_LIST.json"))
    config_list = autogen.config_list_from_json(env_or_file=absolute_path)
    
    # Set up Google Cloud Storage en OpenAI client
    gcp_client = storage.Client()
    client = OpenAI(api_key=config_list[0]["api_key"])
    aiplatform.init(project=PROJECT_ID, location=LOCATION)

    # Function to embed the text using OpenAI API
    def embed_text(text):
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    feature_vector = embed_text(query)

    # Create the index endpoint instance from an existing endpoint.
    my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint(
        index_endpoint_name=INDEX_ENDPOINT
    )

    # Query the index endpoint for the nearest neighbors.
    # The vector search can be filter on faction and source
    # Currently the only data in the index is from the 
    # parliamentary debates or 'PD' source.
    # TODO: Add new sources to the VS index
    resp = my_index_endpoint.find_neighbors(
        deployed_index_id=DEPLOYED_INDEX_ID,
        queries=[feature_vector],
        num_neighbors=topK,
        filter=[
            Namespace("faction", [faction], []),
            Namespace("source", [source], [])
            ]
    )

    print(resp)

    # Extract all the indices from the response
    list_ids = []
    for match in resp[0]:
        list_ids.append(match.id)

    id_set = set(list_ids)

    print(id_set)
    
    output_file_path = 'tmp/'
    os.makedirs(output_file_path, exist_ok=True)

    scrape_bucket_name = f"{PROJECT_ID}_scrape"
    #pd_chunk_directory = "/pd/chunks"
    
    blob_name = "pd/chunks/chunked_512.parquet"
    
    scrape_bucket = gcp_client.get_bucket(scrape_bucket_name)
    
    # Get the blob
    blob = scrape_bucket.blob(blob_name)

    # Download the blob to a local file
    destination_file_name = "chunked_512.parquet"
    blob.download_to_filename(destination_file_name)

    # Read the Parquet file into a DataFrame
    chunked_df = pd.read_parquet("chunked_512.parquet")

    # Print the DataFrame
    print(chunked_df)

    chunked_df.set_index('doc_id', inplace=True)

    print(chunked_df)

    # Use the response to get the document IDs and scores
    filter_df = chunked_df[chunked_df.index.isin(id_set)]
    print(filter_df)
    
    # Add the distances to the DataFrame based on the filtered indices
    for index, row in filter_df.iterrows():
        current_index = row.name
        
        matching_neighbor = None
        for neighbor in resp[0]:
            if neighbor.id == str(current_index):  # Convert index to string for comparison
                matching_neighbor = neighbor
                break
        
        if matching_neighbor:
            filter_df.at[index, 'distance'] = matching_neighbor.distance
        else:
            print(f"Warning: No matching distance found for index {current_index}")
    
    # Sort the DataFrame based on the distance unless it is empty
    if not filter_df.empty:
        filter_df.dropna(subset=['distance'], inplace=True)
        filter_df.sort_values(by='distance', inplace=True)
    else:
        print("Warning: Empty DataFrame")
        filter_df = pd.DataFrame({'id': ['0_0'], 'card_title': 'No title', 'faction': 'No faction', 'text': ['Er zijn geen relevante document gevonden. Vertel dit eerlijk, er zijn geen relevante documenten gevonden. Geef gewoon basis principes terug.'], 'name': 'No one.'})
        filter_df.set_index('id', inplace=True)
    print(filter_df)
    
    output = []
    for index, row in filter_df.iterrows():
        return_string = f'''{row['name']} van {row['faction']} zei over {row['card_title']}: {row['text']} [Bron: {row['download_href']}]'''
        output.append(return_string)
    print(output)   
    return output