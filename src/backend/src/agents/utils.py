from autogen.agentchat.conversable_agent import ConversableAgent

def create_debator(llm_config, faction, message, chunks):
    '''
    This function creates an autogen debator agent for a given faction.
    
    args:
        llm_config: dict, model parameters
        faction: str, name of the faction
        message: str, topic of the debate
        chunks: list, list of chunks to generate a standpoint
    output:
        debator: RetrieveAssistantAgent, debator agent
    '''
    debator = ConversableAgent(
            human_input_mode="NEVER",
            name=faction,
            llm_config=llm_config,
            system_message=f'''
            Je bent een hulpzame AI-assistent.
            
            Je vertegenwoordigt de politieke partij {faction} in een virtueel politiek debat.
            
            Het is jouw taak om het standpunt van de politiek partij {faction} te analyseren.
            Het is jouw taak om hun hart en ziel te begrijpen en een samenvatting te geven van hun standpunt.
            
            Het onderwerp van het debat is: {message}.
            
            Hieronder vind je enkele van hun uitspraken. Gebruik deze informatie om hun standpunt te extraheren.
            Indien je gebruik maakt van een uitspraak, vermeld dan de naam van de persoon en de bron tussen vierkante haken [].
            
            De uitspraken zijn als volgt:
            {' '.join(chunk for chunk in chunks)}.
            
            Doe alsof je hen vertegenwoordigt in een politiek debat.
            Verwijz naar hun uitspraken maar hou het spontaan, vlot en to the point.
            
            Vermeld zeker de naam van je partij: {faction}.
            En de links van de bronnen die je gebruikt, tussen vierkante haken [].
            ''',
            max_consecutive_auto_reply=1,
        )
    print(debator.system_message)
    return debator

def create_summarizer(llm_config, message):
    '''
    This function creates an autogen summarizer agent.
    
    args:
        llm_config: dict, model parameters
        message: str, topic of the debate
    output:
        summarizer: RetrieveAssistantAgent, summarizer agent
    '''
    summarizer = ConversableAgent(
        name="Samenvatter",
        llm_config=llm_config,
        system_message=f'''
        Je bent een hulpzame AI-assistent.
        
        Het is jouw taak om een samenvatting te geven van de standpunten van het debat.
        
        Het onderwerp van het debat is: {message}.
        
        Zorg dat je taalgebruik vlot en toegankelijk is. 
        
        Vermeld alles dat relevant is.
        '''
    )
    return summarizer

def create_coalition_expert(llm_config, message):
    '''
    This function creates an autogen coalition expert agent.
    
    args:
        llm_config: dict, model parameters
        message: str, topic of the debate
    output:
        coalition_expert: RetrieveAssistantAgent, coalition expert agent
    '''
    coalition_expert = ConversableAgent(
        name="Coalitie expert",
        llm_config=llm_config,
        human_input_mode='NEVER',
        system_message=f'''
        Je bent een hulpzame AI-assistent.
        
        Het is jouw taak om een overzicht te geven van de partijen die waarschijnlijk een coalitie zullen vormen.
        
        Baseer jezelf op de samenvatting van het politieke debat.
        
        Het onderwerp van het debat is: {message}.
        '''
    )
    return coalition_expert