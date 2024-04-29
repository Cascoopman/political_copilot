## Fondant
To setup the data pipelines, we used Fondant. 
Fondant is a data framework that enables collaborative dataset building.
It creates such a pipeline by chaining docker containers. These containers are called components and can be taken from the Fondant hub or created yourself. 
Feel free to add another Fondant pipeline.

# Data schema
The data is stored in two formfactors: the original format and the embeddings. 
These formfactors are linked through a unique 'doc_id'. This is crucial as the semantic search will return this 'doc_id' for further processing.
The original format should be a parquet file and should be stored in the '_scrape' bucket. The dataframe containing the data, should have at least the following columns, but additional columns can be added as desired:
            ['faction']: The name of the political faction that this data belongs to
            ['card_title']: Title of the original debate topic 
            ['text']: The actual text of the speech
            ['name']: Containing the name of the person who made the speech
            ['download_href']: An http link to the source

We use a Vertex Vector Search index. Thus for the embedding format we have a strict schema.
This index requires a json file, with each line containing a separate json record created by converting a dataframe, row by row, to this format:

    source = "{PIPELINE_NAME}"

    record = {
        "id": row["doc_id"],
        "embedding": row["embedding"],
        "restricts": [
                {
                    "namespace": "faction",
                    "allow": [row["faction"]]
                },{
                    "namespace": "source",
                    "allow": [source],
                }
            ],
    }
    
    for record in json_records:
        json.dump(record, f)
        f.write('\n')


After setting up the pipelines and adhering to the output schemas, feel free to create a PR.
In case their are issues with setting up a pipeline. You can make use of the manual_data_writer.py helper to load the bucket without Fondant.