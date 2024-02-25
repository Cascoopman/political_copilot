import autogen

from autogen.agentchat.contrib.capabilities import context_handling

config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")

llm_config = {"config_list": config_list, "cache_seed": None}

# Define the ability to manage size of chat history and add it to the agents
manage_chat_history = context_handling.TransformChatHistory(max_tokens_per_message=100, max_messages=10, max_tokens=500)

# User proxy agent
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    code_execution_config=False,
    human_input_mode="NEVER", #TERMINATE, TRUE OR NEVER
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    llm_config=llm_config,
)

# Play around with the voting shares of the factions
PERCENTAGE_CDV="25%"
PERCENTAGE_GROEN="35%"
PERCENTAGE_NVA="40%"

DEFAULT_SYSTEM_MESSAGE = autogen.AssistantAgent.DEFAULT_SYSTEM_MESSAGE

# Assistant agents representing the faction leaders
cdv = autogen.AssistantAgent(
    name="CD&V",
    system_message=DEFAULT_SYSTEM_MESSAGE+"You are the president of CD&V, the centre right catholic political party with "
                    "a voting percentage of " + PERCENTAGE_CDV + ". /n",
    llm_config=llm_config,
)

groen = autogen.AssistantAgent(
    name="Groen",
    system_message=DEFAULT_SYSTEM_MESSAGE+"You are the president of Groen, the green political party focused on nature and people with "
                    "a voting percentage of " + PERCENTAGE_GROEN + ". /n",
                
    llm_config=llm_config,
)
nva = autogen.AssistantAgent(
    name="NVA",
    system_message=DEFAULT_SYSTEM_MESSAGE+"You are the president of the national political party with "
                    "a voting percentage of " + PERCENTAGE_NVA + ". /n",
    llm_config=llm_config,
)
openvld = autogen.AssistantAgent(
    name="OpenVLD",
    system_message="You are the president of the liberal political party.",
    llm_config=llm_config,
)
pvda = autogen.AssistantAgent(
    name="PVDA",
    system_message="You are the president of the progressive political party and are marxistic and populistic.",
    llm_config=llm_config,
)
vlaamsbelang = autogen.AssistantAgent(
    name="Vlaams Belang",
    system_message="You are the president of the rightwing political party and are populistic and nationalistic.",
    llm_config=llm_config,
)
vooruit = autogen.AssistantAgent(
    name="Vooruit",
    system_message="You are the president of the progressive and socialistic political party.",
    llm_config=llm_config,
)


# The groupchat manager allows for speaker selection and conversation routing.
# Left these out for demo purposes: openvld, pvda, vlaamsbelang, vooruit
groupchat = autogen.GroupChat(agents=[cdv, groen, nva], messages=[], allow_repeat_speaker=[], max_round=12, speaker_selection_method="auto")
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
manage_chat_history.add_to_agent(manager)

# Choose the debate topic
TOPIC = "Have a debate about illegal migration."

# Start the debate using an intial prompt
user_proxy.initiate_chat(
    manager, message="This is the beginning of the debate between three parties. \n"
    "Each party will speak for one turn and max 30 words. "
    "It is the task of the presidents to represent their party's view on the topic during the debate. "
    "The topic of this debate is:"
    + TOPIC + "\n"
    "To the presidents: "
    "Consider your parties' positions, their voter support, and how they might compromise or negotiate to reach a consensus on policies and approaches related to the given topic. "
    "Keep in mind the dynamic nature of coalition-building and the need for a balanced outcome that reflects the diverse opinions within the political landscape. "
    "Your answers should contain your party name and political stance. " 
    "Your answers must be as short as possible. "
    "You can mention previous parties in the debate by their name and express your opinion on their stance."
)