from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from google.cloud import firestore
import asyncio

from agents.utils import normalize_message
from agents.manual_debate import run_manual_debate
from agents.async_debate import run_async_debate
from agents.faction_search import faction_search
from agents.vector_search import vector_search
from agents.faction_facts import get_faction_facts
from agents.news_tools import get_news_domestic_politics

app = FastAPI()

# TODO: replace get_news_domestic_politics with tavily_api
# TODO: replace get_faction_facts with vrt searcher https://www.vrt.be/vrtnws/nl/zoek/?query=Partij+Begroting
# TODO: https://www.tijd.be/kieswijzer-2024.html?utm_source=SIM&utm_medium=email&utm_campaign=20240425_TODAY_MORNING_NL_&utm_content=&utm_term=&M_BT=797873122401

async def control_tower(query: str):
    
    timestamp = datetime.now()
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
    
    factions = ["N-VA", "cd&v", "Groen", "Open Vld", "PVDA", "Vlaams Belang", "Vooruit"]
    
    query = normalize_message(query)
    
    chunks_dict = await retrieve(query, factions)
    
    #print(chunks_dict)
    
    #debate =  generate(query, factions, chunks_dict)
    debate = await a_generate(query, factions, chunks_dict)
    #print(debate)
    
    total_time = datetime.now() - timestamp 
    add_log(query, debate, timestamp_str, total_time)
    
    return(debate)

def add_review(stars: int = None, feedback: str = None, json_content: dict = None):
    timestamp = datetime.now()
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
    
    db = firestore.Client(database="political-agents")
    
    # Add data to Firestore
    
    try:
        # Reference to the document
        doc_ref = db.collection("reviews").document(timestamp_str)
        
        # Set data
        doc_ref.set({"stars": stars})
        doc_ref.set({"feedback": feedback}, merge=True)
        doc_ref.set(json_content,merge=True)
        doc_ref.set({"mode": "async"}, merge=True)
        
        print("Data added successfully!")
    except Exception as e:
        print(f"Error adding data: {e}")

    return({"message": "Review added successfully"})

def add_log(query: str, debate: dict, timestamp_str: str, total_time):
    debate['query'] = query
    #TODO: Update mode
    debate['mode'] = 'async'
    debate['total_time'] = total_time.total_seconds()
    db = firestore.Client(database="political-agents")
    
    # Add data to Firestore
    try:
        # Reference to the document
        doc_ref = db.collection("log").document(timestamp_str)
        
        # Set data
        doc_ref.set(debate)
        
        print("Data added successfully!")
    except Exception as e:
        print(f"Error adding data: {e}")

    return({"message": "Log added successfully"})

async def retrieve(query: str, factions: list[str]):
    chunks_dict = {}
    tasks = []
    
    async def search_task(query: str, faction: str):
        list = get_faction_facts(faction)
        list.extend(get_news_domestic_politics(query, topK = 1))
        list.extend(vector_search(query, faction=faction, topK = 3, source = "PD"))
        list.extend(faction_search(query, faction = faction))
        chunks_dict[faction] = list
    
    for faction in factions:
        tasks.append(search_task(query, faction))
        
    await asyncio.gather(*tasks)
    
    return chunks_dict

def generate(query: str, factions, chunks: dict) -> dict:
    response = run_manual_debate(query, factions, chunks)
    return response

async def a_generate(query: str, factions, chunks: dict) -> dict:
    response = await run_async_debate(query, factions, chunks)
    return response

# Define a request body model using Pydantic
class SimulateRequest(BaseModel):
    query: str

# Define a FastAPI endpoint to handle simulate requests
@app.post("/simulate")
async def simulate(request: SimulateRequest):
    response = await control_tower(request.query)
    return response

# Define a request body model using Pydantic
class ReviewRequest(BaseModel):
    stars: int
    feedback: str
    json_content: dict

# Define a FastAPI endpoint to handle debate review requests
@app.post("/review")
async def review(request: ReviewRequest):
    add_review(request.stars, request.feedback, request.json_content)
    response = {"message": "Review added successfully. Thanks!"}
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="0.0.0.0", port=8080)