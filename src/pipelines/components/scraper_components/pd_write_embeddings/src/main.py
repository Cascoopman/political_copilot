import pandas as pd
from fondant.component import PandasTransformComponent
import json
from google.cloud import storage
import os

class WriteToBucket(PandasTransformComponent):
    def __init__(self, *, bucket_name: str, json_file_name: str):
        """Initialize the write to file component."""
        super().__init__()
        self.bucket_name = bucket_name  
        self.json_file_name = json_file_name      

    def transform(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Writes the data from the given Dask DataFrame to a file either locally or
        to a remote storage bucket.

        """
        json_records = WriteToBucket.create_json_records(dataframe)
        dataframe['embedding'] = dataframe['embedding'].apply(lambda x: x.tolist())
        
        output_file_path = 'tmp/'
        os.makedirs(output_file_path, exist_ok=True)
        json_file_path = os.path.join(output_file_path, "embeddings.json")
        json_file = WriteToBucket.create_json_file(json_records, json_file_path)
        
        gcp_client = storage.Client()

        embed_bucket = gcp_client.get_bucket(self.bucket_name)
        
        embed_blob = embed_bucket.blob(self.json_file_name)
        
        embed_blob.upload_from_string(json_file)
        
        return pd.DataFrame({'status': ['We fucking did it baby']})
            
    def create_json_records(df):
        json_records = []
        for index, row in df.iterrows():
            
            # Create JSON record
            record = {
                "id": row["doc_id"],
                "embedding": row["embedding"],
                "restricts": [
                        {
                            "namespace": "faction",
                            "allow": [row["faction"]]
                        },{
                            "namespace": "source",
                            "allow": ["PD"],
                        }
                    ],
            }
            json_records.append(record)
        
        return json_records

    def create_json_file(json_records, json_file_path):
    
        with open(json_file_path, 'w', encoding='utf-8') as f:
            for record in json_records:
                json_string = json.dumps(record)
                f.write(json_string + '\n')
        
        with open(json_file_path, 'r', encoding='utf-8') as f:
            jsonl_content = f.read()
        
        return jsonl_content