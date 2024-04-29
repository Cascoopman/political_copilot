from autogen.agentchat.conversable_agent import ConversableAgent
import os
from openai import OpenAI
import json

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

def create_system_message(faction, message, chunks):
    system_message=f'''
            Je bent een hulpzame AI-assistent.
            
            Je vertegenwoordigt de politieke partij {faction} in een virtueel politiek debat.
            
            Het onderwerp van het debat is: {message}.
            
            Gebruik de onderstaande informatie en bronnen om het standpunt van de partij te formuleren.
            
            Het is jouw taak om het standpunt van de politiek partij {faction} te analyseren, begrijpen en vlot samen te vatten.
            
            Indien je gebruik maakt van een bron, zet deze tussen vierkante haken [Bron :].
            Vermeld ook de persoon die de uitspraak heeft gedaan.
            
            De relevante informatie is als volgt:
            {' '.join(chunk for chunk in chunks)}.
            
            Ter herhaling:
            Vermeld zeker de naam van je partij: {faction}, en de links van de bronnen die je gebruikt tussen vierkante haken [].
            
            Hou je argumentatie spontaan en vlot.
            '''
    return system_message

def normalize_message(query: str):
    # Get OpenAI API key
    current_directory = os.path.dirname(__file__)
    absolute_path = os.path.abspath(os.path.join(current_directory, "OAI_CONFIG_LIST.json"))
    with open(absolute_path, "r") as file:
        config_list = json.load(file)
    
    # Send the URL to openAI
    
    openAI = OpenAI(api_key=config_list[0]["api_key"])
    completion = openAI.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.2,
        messages=[
            {"role": "system", "content": f'''
                Het is aan jou om de input van de gebruiker te modereren en te normaliseren.
                Wij hebben graag een onderwerp voor een virtueel politiek debat.
                De gebruiker kan dit kiezen, maar het moet wel neutraal en respectvol zijn.
                
                Jij moet dus de input omzetten naar een neutraal, relevant, concreet en algemeen debatsonderwerp.
                Maak van korte zinnen een volledige zin.
                Maak van lange zinnen een coherent onderwerp.
                Zet andere talen om in het Nederlands.
                Alle onderwerpen mogen besproken worden, maar insunuerende, beledigende of ongepaste taal zet je om naar een neutrale en respectvolle formulering. 
                Input zoals 'randon', 'test', 'verras me', 'as;dfasdf' enzovoort mag je creatief omzetten naar een relevant debatsonderwerp.
                
                Bijvoorbeeld:
                "Walen uit Belgie" wordt "De onafhankelijkheid van Wallonië ten opzichte van België".
                "nazi's zijn hip" wordt "De opkomst van het nazisme in de jaren 30".
                "The unemployed should be put to work" wordt "Het activeren van werklozen".
                "Er is zojuist een atoombom gevallen" wordt "De gevolgen van een nucleaire aanval".
                "Abortus is hetzelfde als kinderen doden" wordt "De legalisatie van abortus".
                "Les politici sont des voleurs" wordt "De rol van politici in de samenleving".
                "Hoe lossen de partijen het begrotingstekort op" wordt "Aanpakken van het begrotingstekort".
                "Beloftes nakomen" wordt "De rol van politici in de samenleving".
                "Er moet een migratiestop komen" wordt "De migratieproblematiek en migratiestop".
                "Hoe gaan de partijen de stijgende kosten oplossen" wordt "Aanpakken van de stijgende kosten".
                "intelectual property tax advantage voor IT sector" wordt "De belastingvoordelen voor de IT-sector".
                "Ik vraag me echt al een lange tijd af waarom die politiekers zoveel geld verdienen. Die maken veel beloftes en komen ze niet na, waarom betalen we die." wordt "De verloning van politici".
                "Een chatbot dat het parlement vervangt, alle ministers en overheid instanties worden vervangen waar dat mogelijk is" wordt "Het automatiseren en digitaliseren van de overheid".
                
                De gebruiker input is als volgt:
                {query}
                
                Geef enkel het onderwerp van het debat terug, geen andere output.
                '''
                }
            ]
    )
    normalized_message = completion.choices[0].message.content
    print(repr(normalized_message))
    return normalized_message
