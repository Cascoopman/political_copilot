# Political Copilot
## Goal
The goal of this project is to develop a comprehensive tool that helps citizens navigate the political world by leveraging the power of LLM Agents.

The agents can distil government documents, faction websites and news into simple and intuitive answers based on the user's query. Agents allow for larger context windows and their interaction allows for fact checking, grounding and in general a more dynamic and detailed analysis of the political landscape.

The true benefit of using agents is that they each have a tailored RAG system, custom tools, context window and can be entirely parallelized.

## How does it work?
To put it simply, a user query is passed to a moderator, which asks the viewpoints of each faction. This is generated by an agent representing the faction in the virtual debate. After each agent is done generating, a summarizer collects and summarizes the debate before outputting it to the user. 

Here's a demo!

![demo_square_highres](https://github.com/jBontinck/political_copilot/assets/58267444/fbee7c7b-4cd6-45dc-b0e3-a37f97fb3f3e)


To put it less simply, the system first creates the agents based on data about the faction representing its history and values. The agent that embodies the faction then collects data that is relevant for generating a stance on the user query. Before or after generating a viewpoint, each agent has to ability to call upon other tools. These tools can be shared, reusable components or private custom tools. Other agents can also be wrapped inside a tool. Finally, their generated responses are further processed to fact check, add sources and return a coherent output.

As for the tech-stack, we use [Fondant](https://fondant.ai/en/latest/) to create data pipelines. This tools allows for easy collaboration when crafting big data. The data for the RAG is chunked, embedded and stored in a GCP Vector Search according to a [specific JSON schema](https://cloud.google.com/vertex-ai/docs/vector-search/setup/format-structure#input_data_storage_and_file_organization). We explored the [Autogen](https://github.com/microsoft/autogen/tree/main) library, it has different agent orchestration methods. But ultimately, our standard conversation is a hard-coded single turn debate where the agents do not see the output of other agents. Finally, we use [Streamlit](https://github.com/streamlit/streamlit) to create the User Interface where we return the output to the user. The entire system's cloud infrastructure is built using [Nimbus](https://www.ml6.eu/domains/infrastructure), an ML6 in-house cloud deployment boilerplate, and [Terraform](https://www.terraform.io/).

## How can I contribute?
There are two key parts in this system: the data and the agents. 

This tool depends heavily on the quality and amount of data it is fed. You can add data to the [Vector DB](https://github.com/jBontinck/political_copilot/tree/main/src/pipelines). We welcome any data that adheres to the prescribed schemas. Or you can add data from within a tool call.

Which brings us to the agents. You can add [tools or orchestration methods](https://github.com/jBontinck/political_copilot/tree/main/src/backend/src).

## Codebase 
Before you can deploy this system, make sure to first setup the Vector Search, the backend and the frontend. To actually deploy or undeploy the system, run the deploy and undeploy scripts. Be sure to first set your $GCP_PROJECT_NAME, $GCP_VS_INDEX and $GCP_VS_ENDPOINT variables.

## Architecture
![Excalidraw_architecture](https://github.com/jBontinck/political_copilot/assets/58267444/8e5fc87c-b1d8-4ef1-b46d-137459250cb1)

_For questions or feedback, contact us at:_
_jensbontinck@gmail.com_ and
_cascoopman@hotmail.com_
