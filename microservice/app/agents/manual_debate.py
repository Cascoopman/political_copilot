# Import necessary libraries
import autogen
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent

import chromadb

import os

# To disable an error
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Reads information about where the local model is
# We act as if this model is GPT
config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")

# Model parameters
llm_config={
    "timeout": 600,
    "seed": None,
    "config_list": config_list,
    "temperature": 0,
}

# Ask the user for the topic of the debate
message = input("What is the topic of the debate? ")

# Initialize the faction agents and their retrieval agents
debator_vooruit = RetrieveAssistantAgent(
    name="Vooruit",
    llm_config=llm_config,
    system_message=f'''
    You are a helpful AI assistant. 
    It is your task analyze the documents of the political party 'Vooruit'.
    Return an overview of their stance on the topic: {message}.
    If you can't properly respond to the topic with or without the current context, you should reply exactly `UPDATE CONTEXT`.
    Base yourself only on the documents.
    Keep it as brief and short as possible.
    Start by mentioning the name 'Vooruit'.
    ''',
)
retriever_vooruit = RetrieveUserProxyAgent(
    name="retriever_Vooruit",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "debate",
        "docs_path": None,
        "chunk_token_size": 1500,
        "model": config_list[0]["model"],
        "client": chromadb.PersistentClient(path="/Users/cas/political_agents/backend/scrapers/FactionWebsites/data/db"),
        "collection_name" : "vooruit",
        "embedding_model": "distiluse-base-multilingual-cased-v2",
        "get_or_create": True, 
    },
    code_execution_config=False,
)

debator_groen = RetrieveAssistantAgent(
    name="Groen",
    llm_config=llm_config,
    system_message=f'''
    You are a helpful AI assistant. 
    It is your task analyze the documents of the political party 'Groen'.
    Return an overview of their stance on the topic: {message}.
    If you can't properly respond to the topic with or without the current context, you should reply exactly `UPDATE CONTEXT`.
    Base yourself only on the documents.
    Keep it as brief and short as possible.
    Start by mentioning the name 'Groen'.
    ''',
)
retriever_groen = RetrieveUserProxyAgent(
    name="retriever_Groen",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "debate",
        "docs_path": None,
        "chunk_token_size": 1500,
        "model": config_list[0]["model"],
        "client": chromadb.PersistentClient(path="/Users/cas/political_agents/backend/scrapers/FactionWebsites/data/db"),
        "collection_name" : "groen",
        "embedding_model": "distiluse-base-multilingual-cased-v2",
        "get_or_create": True, 
    },
    code_execution_config=False, 
)

debator_cdv = RetrieveAssistantAgent(
    name="CD&V",
    llm_config=llm_config,
    system_message=f'''
    You are a helpful AI assistant. 
    It is your task analyze the documents of the political party 'CD&V'.
    Return an overview of their stance on the topic: {message}.
    If you can't properly respond to the topic with or without the current context, you should reply exactly `UPDATE CONTEXT`.
    Base yourself only on the documents.
    Keep it as brief and short as possible.
    Start by mentioning the name 'CD&V'.
    ''',
)
retriever_cdv = RetrieveUserProxyAgent(
    name="retriever_CD&V",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "debate",
        "docs_path": None,
        "chunk_token_size": 1500,
        "model": config_list[0]["model"],
        "client": chromadb.PersistentClient(path="/Users/cas/political_agents/backend/scrapers/FactionWebsites/data/db"),
        "collection_name" : "cdv",
        "embedding_model": "distiluse-base-multilingual-cased-v2",
        "get_or_create": True, 
    },
    code_execution_config=False, 
)

debator_nva = RetrieveAssistantAgent(
    name="NVA",
    llm_config=llm_config,
    system_message=f'''
    You are a helpful AI assistant. 
    It is your task analyze the documents of the political party 'NVA'.
    Return an overview of their stance on the topic: {message}.
    If you can't properly respond to the topic with or without the current context, you should reply exactly `UPDATE CONTEXT`.
    Base yourself only on the documents.
    Keep it as brief and short as possible.
    Start by mentioning the name 'NVA'.
    ''',
)
retriever_nva = RetrieveUserProxyAgent(
    name="retriever_NVA",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "debate",
        "docs_path": None,
        "chunk_token_size": 1500,
        "model": config_list[0]["model"],
        "client": chromadb.PersistentClient(path="/Users/cas/political_agents/backend/scrapers/FactionWebsites/data/db"),
        "collection_name" : "nva",
        "embedding_model": "distiluse-base-multilingual-cased-v2",
        "get_or_create": True, 
    },
    code_execution_config=False, 
)

debator_openvld = RetrieveAssistantAgent(
    name="Open VLD",
    llm_config=llm_config,
    system_message=f'''
    You are a helpful AI assistant. 
    It is your task analyze the documents of the political party 'Open VLD'.
    Return an overview of their stance on the topic: {message}.
    If you can't properly respond to the topic with or without the current context, you should reply exactly `UPDATE CONTEXT`.
    Base yourself only on the documents.
    Keep it as brief and short as possible.
    Start by mentioning the name 'Open VLD'.
    ''',
)
retriever_openvld = RetrieveUserProxyAgent(
    name="retriever_Open_VLD",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "debate",
        "docs_path": None,
        "chunk_token_size": 1500,
        "model": config_list[0]["model"],
        "client": chromadb.PersistentClient(path="/Users/cas/political_agents/backend/scrapers/FactionWebsites/data/db"),
        "collection_name" : "openvld",
        "embedding_model": "distiluse-base-multilingual-cased-v2",
        "get_or_create": True, 
    },
    code_execution_config=False, 
)

debator_pvda = RetrieveAssistantAgent(
    name="PVDA",
    llm_config=llm_config,
    system_message=f'''
    You are a helpful AI assistant. 
    It is your task analyze the documents of the political party 'PVDA'.
    Return an overview of their stance on the topic: {message}.
    If you can't properly respond to the topic with or without the current context, you should reply exactly `UPDATE CONTEXT`.
    Base yourself only on the documents.
    Keep it as brief and short as possible.
    Start by mentioning the name 'PVDA'.
    ''',
)
retriever_pvda = RetrieveUserProxyAgent(
    name="retriever_PVDA",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "debate",
        "docs_path": None,
        "chunk_token_size": 1500,
        "model": config_list[0]["model"],
        "client": chromadb.PersistentClient(path="/Users/cas/political_agents/backend/scrapers/FactionWebsites/data/db"),
        "collection_name" : "pvda",
        "embedding_model": "distiluse-base-multilingual-cased-v2",
        "get_or_create": True, 
    },
    code_execution_config=False, 
)

debator_vlaamsbelang = RetrieveAssistantAgent(
    name="Vlaams_Belang",
    llm_config=llm_config,
    system_message=f'''
    You are a helpful AI assistant. 
    It is your task analyze the documents of the political party 'Vlaams Belang'.
    Return an overview of their stance on the topic: {message}.
    If you can't properly respond to the topic with or without the current context, you should reply exactly `UPDATE CONTEXT`.
    Base yourself only on the documents.
    Keep it as brief and short as possible.
    Start by mentioning the name 'Vlaams Belang'.
    ''',
)
retriever_vlaamsbelang = RetrieveUserProxyAgent(
    name="retriever_Vlaams_Belang",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "debate",
        "docs_path": None,
        "chunk_token_size": 1500,
        "model": config_list[0]["model"],
        "client": chromadb.PersistentClient(path="/Users/cas/political_agents/backend/scrapers/FactionWebsites/data/db"),
        "collection_name" : "vlaamsbelang",
        "embedding_model": "distiluse-base-multilingual-cased-v2",
        "get_or_create": True, 
    },
    code_execution_config=False, 
)

# Initialize a rerouting agent named chat manager
chat_manager = autogen.AssistantAgent(
    name="Chat_manager",
    llm_config=False,
)

# Initialize the summarizer agent
summarizer = autogen.AssistantAgent(
    name="Summarizer",
    llm_config=llm_config,
    system_message=f'''
    You are a helpful AI assistant that is an expert in writing summaries.
    It is your task summarize the viewpoints of the individual political party's.
    The topic of the debate is: {message}.
    Compare the viewpoints of the political party's by giving their similarities, differences and an overall conclusion.
    Try to keep it brief and short.
    ''',
)

# Initialize the coalition expert
coalition = autogen.AssistantAgent(
    name="Coalition_expert",
    llm_config=llm_config,
    system_message=f'''
    You are a helpful AI assistant that is an expert in estimating coalition partners.
    Based yourself on the summary of the political debate.
    The topic of the debate is: {message}.
    You should return an overview of the party's that are likely going to create a coalition.
    Try to keep it brief and short.
    ''',
)

# Group the debators and retrievers
debators = [debator_vooruit, debator_groen, debator_cdv, debator_nva, debator_openvld, debator_pvda, debator_vlaamsbelang]
retrievers = [retriever_vooruit, retriever_groen, retriever_cdv, retriever_nva, retriever_openvld, retriever_pvda, retriever_vlaamsbelang]

# Generate the party's defenses
for i in range(0,len(debators)):
    retrievers[i].initiate_chat(debators[i],problem=message,silent=True)
    chat_manager.receive(message=debators[i].last_message(),sender=debators[i],request_reply=False,silent=True)

# Generate the summary
for i in range(0,len(debators)-1):
    chat_manager.send(chat_manager.last_message(agent=debators[i]),recipient=summarizer,request_reply=False,silent=True)
chat_manager.send(chat_manager.last_message(agent=debators[-1]),recipient=summarizer,request_reply=True,silent=True)

# Generate the coalition estimation
coalition.receive(message=summarizer.last_message(),sender=chat_manager,request_reply=True)