from google.cloud import storage
from google.cloud import aiplatform
from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import Namespace
from openai import OpenAI
import os

# Define environment variables
PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
LOCATION = 'europe-west1'

# Set variables for the current deployed index.
INDEX_ENDPOINT="projects/429336914421/locations/europe-west1/indexEndpoints/6945474215172636672"
DEPLOYED_INDEX_ID="political_endpoint"

# Set up Google Cloud Storage en OpenAI client
gcp_client = storage.Client()
client = OpenAI()

# Function to embed the text using OpenAI API
def embed_text(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

# Define the search query and embed it aswell
query = 'Wat is nu de uitkomst van de situatie bij De Lijn?'
feature_vector = embed_text(query)

# Create the index endpoint instance from an existing endpoint.
my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint(
    index_endpoint_name=INDEX_ENDPOINT
)

# my_index_endpoint.deploy_index(deployed_index_id=DEPLOYED_INDEX_ID)

# TODO add the filter
# Query the index endpoint for the nearest neighbors.
resp = my_index_endpoint.find_neighbors(
    deployed_index_id=DEPLOYED_INDEX_ID,
    queries=[feature_vector],
    num_neighbors=10,
    filter=[
        Namespace("faction", ["groen"]),
        Namespace("source", ["PD"]),
        ],
)

print(resp)

# Extract all the indices from the response
list_ids = []
for match in resp[0]:
    list_ids.append(int(match.id))

id_set = set(list_ids)

# Use the response to get the document IDs and scores
filter_df = chunked_df[chunked_df['index'].isin(id_set)]

# Add the distances to the DataFrame based on the filtered indices
for index, row in filter_df.iterrows():
    current_index = row['index']
    
    matching_neighbor = None
    for neighbor in resp[0]:
        if neighbor.id == str(current_index):  # Convert index to string for comparison
            matching_neighbor = neighbor
            break
    
    if matching_neighbor:
        filter_df.at[index, 'distance'] = matching_neighbor.distance
    else:
        print(f"Warning: No matching distance found for index {current_index}")

filter_df.sort_values(by='distance', inplace=True)
print(filter_df)


#my_index_endpoint.undeploy_index(deployed_index_id=DEPLOYED_INDEX_ID)