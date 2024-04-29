import os
import asyncio
import json
from openai import AsyncOpenAI
from agents.utils import create_system_message

async def run_async_debate(query, factions, chunks_dict) -> dict:
    '''
    This function runs an async debate between the political factions.
    Each faction will be asked to provide a summary of their stance on a given topic.
    They cannot see eachothers viewpoints.
    Finally a summarizer will summarize the viewpoints and
    a coalition expert will estimate the coalition partners.
    
    args:
        query: str, the query to debate about
        factions: list, the factions participating in the debate
        chunks_dict: dict, chunks retrieved from the index with the faction as key
    '''
    # To disable an error
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    
    # Get OpenAI API key
    current_directory = os.path.dirname(__file__)
    absolute_path = os.path.abspath(os.path.join(current_directory, "OAI_CONFIG_LIST.json"))
    with open(absolute_path, "r") as file:
        config_list = json.load(file)

    # Init vars
    a_openAI = AsyncOpenAI(api_key=config_list[0]["api_key"])
    tasks = []
    responses = {}
    
    # Async function to create response
    async def async_response(messages, responses, faction):
            response = await a_openAI.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=messages,
                temperature=0.0,
            )
            lowercase_faction = faction.lower().replace(" ", "").replace("-", "").replace("&", "")
            responses[lowercase_faction] = response.choices[0].message.content
            
    # Generate all faction viewpoints in parallel
    for faction in factions:
        message = create_system_message(faction, query, chunks_dict[faction])
        
        messages=[
            {"role": "system", "content": message}
        ]
        
        tasks.append(async_response(messages, responses, faction))
    
    # Wait for them to finish
    await asyncio.gather(*tasks)    

    # Initialize the summarizer agent with gpt 4
    stemkiezer = await a_openAI.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", 
                     "content": f'''
                        Je bent een hulpzame AI-assistent.
                        
                        Het is jouw taak om de standpunten van de politieke partijen te groeperen op relevant assen naar keuze.
                        Deze assen kunnen zijn sociaal, economisch, ecologisch, enz.
                        Gebruik een as dat relevant is voor het onderwerp: {query}.
                        Vergelijk alle partijen, groepeer en sorteer ze op basis van hun standpunten.
                        
                        Maak de tekst zeer toegankelijk, vlot leesbaar en begrijpelijk.
                        Gebruik geen bullet points of lijsten, maar maak een vloeiende tekst.
                        
                        Vertel welke partijen overeenkomen en welke niet.
                        Vertel ook waar de partijen zich bevinden op vlak van het onderwerp.
                        
                        Geef daarbij ook een samenvatting van de standpunten van het debat per partij.
                        Het onderwerp van het debat is: {query}.
                        
                        Zorg dat je taalgebruik vlot en toegankelijk is. 
                        Vermeld alle argumenten die relevant zijn.
                        Hieronder is het politieke debat in JSON formaat:
                        {responses}
                    '''}
                ],
                temperature=0.0,
            )
    
    responses["summary"] = stemkiezer.choices[0].message.content
    
    #coalition_expert = create_coalition_expert(llm_config, query)
    # Generate the party's defenses
    responses["coalition"] = "empty for now"
    print(responses)
    return responses