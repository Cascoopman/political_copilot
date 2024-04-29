The default Agent conversation pattern can be seen in manual_debate.py.
This conversation pattern allows each faction to generate a viewpoint using RAG.
The summarizer returns a summary of their responses.

Be sure to add a new file OAI_CONFIG_LIST.json in the agents folder, that contains a list with a dict for every model type you want to use for your agents. E.g.:
    [
        {
            "model": "gpt-3.5-turbo",  
            "api_key": "//" 
        },
        {
            "model": "mistral7b",
            "api_key": "//"
        }
    ]


To add custom conversation patterns, feel free to create a PR containing a new conversation_pattern.py file.
The function that starts the conversation has access to three variables:
    query: str, the query to debate about
    factions: list, the factions participating in the debate
    chunks_dict: dict, chunks retrieved from the index with the faction as key

The output of the function should be a dict.
    responses: dict, a dict containing responses with as key the source and as value the message of the source.

For example:
    responses = {
        'summary': 'This message is output by the summary agent and contains the summary of the debate',
        'groen': 'Our faction believes that...',
        'openvld': 'As Open VLD, we sincerely hope that ...',
        ...
    }