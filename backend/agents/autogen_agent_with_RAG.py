import autogen

from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent

import chromadb

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")

llm_config={
    "timeout": 600,
    "seed": None,
    "config_list": config_list,
    "temperature": 0,
}

DEFAULT_SYSTEM_MESSAGE = autogen.AssistantAgent.DEFAULT_SYSTEM_MESSAGE

assistant = RetrieveAssistantAgent(
    name="assistant",
    system_message="You are a helpful assistant.",
    llm_config=llm_config,
)

ragproxyagent = RetrieveUserProxyAgent(
    name="ragproxyagent",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "qa",
        "docs_path": None,
        "chunk_token_size": 1500,
        "model": config_list[0]["model"],
        "client": chromadb.PersistentClient(path="/Users/cas/political_agents/backend/scrapers/FactionWebsites/data/db"),
        "collection_name" : "vooruit",
        "embedding_model": "distiluse-base-multilingual-cased-v2",
        "get_or_create": True,  # set to False if you don't want to reuse an existing collection, but you'll need to remove the collection manually
    },
    code_execution_config=False,  # set to False if you don't want to execute the code
)

qa_problem = "What is the name of the president (in Dutch 'Voorzitter') of the faction Vooruit?"
ragproxyagent.initiate_chat(assistant, problem=qa_problem)