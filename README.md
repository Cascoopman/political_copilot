# Political Copilot
## Goal
The goal of this project is to develop a comprehensive tool that helps citizens navigate the political world by leveraging the power of Agents.

The agents can distil complex and recent government documents and turn them into simple and intuitive answers to a user's query. Having the agents interact with eachother allows for fact checking, grounding and in general a very dynamic analysis of the political landscape.

## Why?
We believe that citizens have the right to be informed. This tool allows them to digest and interact with the vast ocean of political data out there. We are certain that informed citizens contribute their vote to a welfaring society.

## How does it work?
To put it simply, our tool extracts the data that is most similar to the user's query. This data is then fed into the prompt of agents. The agents then generate a viewpoint based on this data. Finally, their responses are further processed to return a coherent output.

To put it less simply, each agent is a separate RAG system. We use Fondant (https://fondant.ai/en/latest/) to create data pipelines. This tools allows for easy collaboration when crafting big data. The data for the RAG is chunked, embedded and stored in a GCP Vector Search according to a specific schema. We use the Autogen library to orchestrate how these agents communicate and debate with eachother. Finally, we use streamlit to return the output to the user. The entire system's cloud infrastructure is built using Nimbus and Terraform.

## How can I contribute?
There are two key parts in this system: the data and the agents. 
This tool depends heavily on the quality and amount of data it is fed.

We welcome any data that adheres to the prescribed schema. (See Src > Pipelines > README.md)

We welcome new agent capabilities such as tool calling, agent orchestration methods and more. (See Src > Backend > Src > Agents > README.md)

## Codebase
Before you can deploy this system, make sure to first setup the Vector Search, the backend and the frontend. To actually deploy or undeploy the system, run the deploy and undeploy scripts. Be sure to first set your $GCP_PROJECT_NAME, $GCP_VS_INDEX and $GCP_VS_ENDPOINT variables.

## Architecture
https://excalidraw.com/#room=fd1249eeae9767cd4ba5,_r7YsTSTZlldzadTgBR0lQ

_For questions or feedback, contact us at:_
_jensbontinck@gmail.com_
_cascoopman@hotmail.com_