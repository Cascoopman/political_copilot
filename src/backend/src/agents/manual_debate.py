import autogen
from autogen import UserProxyAgent
import os
from agents.utils import create_debator, create_summarizer, create_coalition_expert

def run_manual_debate(query, factions, chunks_dict) -> dict:
    '''
    This function runs a manual debate between the political factions.
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
    current_directory = os.path.dirname(__file__)
    absolute_path = os.path.abspath(os.path.join(current_directory, "OAI_CONFIG_LIST.json"))

    # Grab configuration list containing key and model type
    config_list = autogen.config_list_from_json(env_or_file=absolute_path)

    # Additional model parameters
    llm_config={
        "timeout": 600,
        "seed": None,
        "config_list": config_list,
        "temperature": 0,
    }

    def generate_debators(llm_config, factions, query, chunks_dict):
        debators = {}
        for faction in factions:
            lowercase_faction = faction.lower().replace(" ", "").replace("-", "").replace("&", "")
            debator_name = f"{lowercase_faction}"
            debators[debator_name] = create_debator(llm_config, faction, query, chunks_dict[faction])
            print(chunks_dict[faction])
            print(debators[debator_name].system_message)
        return debators

    # Generate the debators
    debators = generate_debators(llm_config, factions, query, chunks_dict)
    
    user_proxy = UserProxyAgent(
        name="user_proxy",
        llm_config=False,
        code_execution_config=False,
        is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
    )
    
    # Initialize a simple routing agent named chat manager
    chat_manager = autogen.AssistantAgent(
        name="Chat_manager",
        llm_config=False,
    )

    # Initialize a summarizer agent
    summarizer = create_summarizer(llm_config, query)
    coalition_expert = create_coalition_expert(llm_config, query)
    # Generate the party's defenses
    
    responses = {}
    
    for name, debator in debators.items():
        user_proxy.initiate_chat(message=query, recipient=debator, request_reply=True, silent=False)
        
    for name, debator in debators.items():
        responses[name] = user_proxy.last_message(debator)['content']
        chat_manager.receive(message=debator.last_message(),sender=debator,request_reply=False,silent=True)

    
    dict_length = len(debators)
    
    # Generate the summary, the last debator will invoke the summarizer
    for index, (_, debator) in enumerate(debators.items()):
        if index != dict_length - 1:
            chat_manager.send(chat_manager.last_message(agent=debator),recipient=summarizer,request_reply=False,silent=True)
        else: 
            chat_manager.send(chat_manager.last_message(agent=debator),recipient=summarizer,request_reply=True,silent=True)
            print(summarizer.last_message()['content'])
    
    responses["summary"] = summarizer.last_message()['content']
    
    print(responses)
    
    # Generate the coalition estimation
    coalition_expert.receive(message=summarizer.last_message(),sender=chat_manager,request_reply=True)
    
    print(coalition_expert.last_message())
    responses["coalition"] = coalition_expert.last_message()['content']
    return responses