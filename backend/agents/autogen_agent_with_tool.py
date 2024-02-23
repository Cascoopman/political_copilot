import autogen
from autogen.cache import Cache

from IPython import get_ipython
from typing_extensions import Annotated

# LLM parameters:
# some versions of autogen require the "api_base" entity, other versions require 
# the base_url entity. Both return the link to the model / api
config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")

llm_config={
    "timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0,
}

# Declaring the assistant and the Agent:

coder = autogen.AssistantAgent(
    name="chatbot",
    system_message="For stopwatch tasks, call the stopwatch function you have been provided with." + 
    "For coding tasks, use the python function you have been provided with.",
    llm_config=llm_config,
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    system_message="A proxy for the user for executing code. Be sure to reply TERMINATE when the task is done, this is very important.",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={
        "work_dir": "agent_output",
        "use_docker": False,
    },
    llm_config=llm_config,
    )

# Define the functions according to the function description:

def exec_python(cell: Annotated[str, "Valid Python cell to execute."]) -> str:
    ipython = get_ipython()
    result = ipython.run_cell(cell)
    log = str(result.result)
    if result.error_before_exec is not None:
        log += f"\n{result.error_before_exec}"
    if result.error_in_exec is not None:
        log += f"\n{result.error_in_exec}"
    return log

autogen.agentchat.register_function(
    exec_python,
    caller=coder,
    executor=user_proxy,
    name="python_sh",
    description="run a shell script and return the execution result.",
)

with Cache.disk() as cache:
    # start the conversation
    user_proxy.initiate_chat(
        coder,
        message="Run a stopwatch for 5 seconds.",
        cache=cache,
    )