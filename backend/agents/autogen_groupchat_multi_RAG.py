import autogen
from typing_extensions import Annotated

from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen.agentchat.contrib.capabilities import context_handling

import chromadb
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")
manage_chat_history = context_handling.TransformChatHistory(max_tokens_per_message=30, max_messages=10, max_tokens=300)

# Ask the user their question
topic = input("Please enter the topic of the debate: ")


llm_config={
    "timeout": 600,
    "seed": None,
    "config_list": config_list,
    "temperature": 0,
}

# Define the termination detection function
def termination_msg(x):
    return 'TERMINATE' in str(x.get("content", ""))

# Define the proxy agent for the user interaction
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    description="Acts as a proxy for the user, capable of executing code and handling user interactions within predefined guidelines.",
    is_termination_msg=termination_msg,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "/agent_output",
                           "use_docker": False},
)

# Define the debate moderator
moderator = autogen.AssistantAgent(
    name="Moderator",
    description="Guides the debate.",
    llm_config=llm_config,
    system_message=f'''
    You are the Moderator of the debate. 
    Ensure that each party can express their opinion. 
    Act as a communication hub, maintain order and guide the debate. 
    You must only announce either the beginning of the debate, the next speaker, or the debate has ended.
    Terminate the conversation with "TERMINATE" when each political party has been able to speak.
    '''
)

PROMPT_QA = """You're a retrieve augmented chatbot. You answer user's questions based on your own knowledge and the
context provided by the user.
If you can't answer the question with or without the current context, you should reply exactly `UPDATE CONTEXT`.
You must give as short an answer as possible."""

# Define the debator agent for the CD&V
cdv_debator = autogen.AssistantAgent(
    name="CD&V_Debator",
    description="Debator representing the CD&V.",
    llm_config=llm_config,
    system_message=f'''
    As a professional debator, your key task is to represent the political party CD&V.
    CD&V is the centre right catholic political party in Flanders, Belgium. 
    Give the party's viewpoint on the debate topic: {topic}.
    Before responding, gather relevant content using the provided tool. 
    You can invoke this tool by saying "UPDATE CONTEXT".
    Important, first gain more information on the party's opinions using the provided tool.
    Use the provided retrieval tool to support your claims with facts. 
    Coordinate closely with the Moderator to ensure the debate runs smoothly. 
    Conclude with "TERMINATE" once you have communicated the party's viewpoint on the topic.
    '''    
)

# Define the retriever agent for the CD&V
cdv_ragproxyagent = RetrieveUserProxyAgent(
    name="CD&V_Researcher",
    description="Assistant who has extra content retrieval power for solving difficult problems.",
    is_termination_msg=termination_msg,
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
        "get_or_create": True,  # set to False if you don't want to reuse an existing collection, but you'll need to remove the collection manually
    },
    code_execution_config=False,  # set to False if you don't want to execute the code
)

# Define the debator agent for Groen
groen_debator = autogen.AssistantAgent(
    name="Groen_Debator",
    description="Debator representing Groen.",
    llm_config=llm_config,
    system_message=f'''
    As a professional debator, your key task is to represent the political party Groen.
    Groen is the ecological and socialistic party in Flanders, Belgium. 
    Give the party's viewpoint on the debate topic: {topic}.
    Before responding, gather relevant content using the provided tool call retrieve_content. 
    Use the information from your party's Researcher.
    Coordinate closely with the Moderator to ensure the debate runs smoothly. 
    Conclude with "TERMINATE" once you have communicated the party's viewpoint on the topic.
    '''    
)

# Define the retriever agent for Groen
groen_ragproxyagent = RetrieveUserProxyAgent(
    name="Groen_Researcher",
    description="Assistant who has extra content retrieval power for solving difficult problems.",
    is_termination_msg=termination_msg,
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
        "get_or_create": True,  # set to False if you don't want to reuse an existing collection, but you'll need to remove the collection manually
    },
    code_execution_config=False,  # set to False if you don't want to execute the code
)

# Give the agents the capability to shorten chat history to ensure context window compliance
#manage_chat_history.add_to_agent(cdv_debator)
#manage_chat_history.add_to_agent(groen_debator)

# Wrap the party retrieval agents as a function that can be called by the debators
def cdv_retrieve_content(
    message: Annotated[
        str,
        "Refined message which keeps the original meaning and can be used to retrieve content for argumentation.",
    ],
    n_results: Annotated[int, "number of results"] = 2,
) -> str:
    cdv_ragproxyagent.n_results = n_results  # Set the number of results to be retrieved.
    # Check if we need to update the context.
    update_context_case1, update_context_case2 = cdv_ragproxyagent._check_update_context(message)
    if (update_context_case1 or update_context_case2) and cdv_ragproxyagent.update_context:
        cdv_ragproxyagent.problem = message if not hasattr(cdv_ragproxyagent, "problem") else cdv_ragproxyagent.problem
        _, ret_msg = cdv_ragproxyagent._generate_retrieve_user_reply(message)
    else:
        ret_msg = cdv_ragproxyagent.generate_init_message(message, n_results=n_results)
    return ret_msg if ret_msg else message

autogen.agentchat.register_function(
    cdv_retrieve_content,
    caller=cdv_debator,
    executor=cdv_ragproxyagent,
    name="CDV_Retrieval_tool",
    description="Retrieve your party's content for debate argumentation.",
)

# Assign the function to the debator
#for caller in [cdv_debator]:
#    d_retrieve_content = caller.register_for_llm(
#        description="retrieve your party's content for debate argumentation.", api_style="tool"
#    )(cdv_retrieve_content)
#for executor in [user_proxy]:
#    executor.register_for_execution()(d_retrieve_content)

def groen_retrieve_content(
    message: Annotated[
        str,
        "Refined message which keeps the original meaning and can be used to retrieve content for argumentation.",
    ],
    n_results: Annotated[int, "number of results"] = 2,
) -> str:
    groen_ragproxyagent.n_results = n_results  # Set the number of results to be retrieved.
    # Check if we need to update the context.
    update_context_case1, update_context_case2 = groen_ragproxyagent._check_update_context(message)
    if (update_context_case1 or update_context_case2) and groen_ragproxyagent.update_context:
        groen_ragproxyagent.problem = message if not hasattr(groen_ragproxyagent, "problem") else groen_ragproxyagent.problem
        _, ret_msg = groen_ragproxyagent._generate_retrieve_user_reply(message)
    else:
        ret_msg = groen_ragproxyagent.generate_init_message(message, n_results=n_results)
    return ret_msg if ret_msg else message

# Assign the function to the debator
for caller in [groen_debator]:
    d_retrieve_content = caller.register_for_llm(
        description="retrieve your party's content for debate argumentation.", api_style="tool"
    )(groen_retrieve_content)
for executor in [user_proxy]:
    executor.register_for_execution()(d_retrieve_content)

# Reset agents for fresh conversation
def _reset_agents():
    moderator.reset()
    cdv_debator.reset()
    groen_debator.reset()
    user_proxy.reset()

_reset_agents()

# Construct the groupchat and its routing rules
groupchat = autogen.GroupChat(
    agents=[moderator, cdv_debator, cdv_ragproxyagent, user_proxy, groen_debator, groen_ragproxyagent],
    messages=[],
    max_round=12,
    speaker_selection_method="manual",
    allow_repeat_speaker=True,
)

# The manager is an LLM that chooses the next speaker. 
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Start chatting with the user proxy agent.
user_proxy.initiate_chat(
    manager,
    message=f'''The topic of the debate is {topic}''',
)
# Condense previous work and only return specific information
user_proxy.stop_reply_at_receive(manager)
user_proxy.send(f'''
                Give me a summary of the debate, return ONLY the debate, 
                and add TERMINATE in the end of the message''', 
                manager)

# return the last message the expert received
print(user_proxy.last_message()["content"])