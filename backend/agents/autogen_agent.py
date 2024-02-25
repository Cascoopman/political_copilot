import autogen

# LLM parameters
config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")

llm_config={
    "timeout": 600,
    "seed": None,
    "config_list": config_list,
    "temperature": 0,
}

# Declaring the assistant and the Agent (Same LLM config)
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
)

agent = autogen.UserProxyAgent(
    name="agent",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "agent_output",
        "use_docker": False,
    },
    llm_config=llm_config,
    )

prompt = (
    "Find all $x$ that satisfy the inequality $(2x+10)(x+3)<(3x+9)(x+8)$. Express your answer in interval notation."
)

agent.initiate_chat(assistant, clear_history=True, message=prompt)