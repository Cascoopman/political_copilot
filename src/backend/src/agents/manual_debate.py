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
        chunks: dict, chunks retrieved from the index
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

'''
# Test the function
# TODO: Parallellize
run_manual_debate(query="De situatie met de bussen van De Lijn", 
                  factions = ["Open VLD", "Groen", "cd&v"],
                    chunks_dict={
                    "Open VLD": ['\n            Willem-Frederik Schiltz (Open Vld) van de politieke partij Open Vld \n            heeft het volgende gezegd over  over de actuele situatie bij De Lijn: op tafel liggen, we ervoor open staan om daarnaar te kijken. Wat kunt u nu nog meer vragen? (Applaus bij de meerderheid) \n            ', '\n            Minister Lydia Peeters van de politieke partij Open Vld \n            heeft het volgende gezegd over  over de actuele situatie bij De Lijn: twee weken, in een gedachtewisseling over alle details en vragen samen met De Lijn zelf. We zullen er nog heel veel over debatteren, maar we blijven controleren, klachten verzamelen, evalueren, monitoren en bijsturen. Dat is mijn antwoord daarop. \n            ', '\n            Minister Gwendolyn Rutten van de politieke partij Open Vld \n            heeft het volgende gezegd over  over de actuele situatie bij De Lijn: stuk moet worden uitgerold, dan gaan we dat gewoon doen. \n            ', '\n            Marino Keulen (Open Vld) van de politieke partij Open Vld \n            heeft het volgende gezegd over  over de actuele situatie bij De Lijn: goed te keuren. Dat is uw eigen verantwoordelijkheid. Wat de budgetten betreft, ook daar is er het stappenplan. Geef eerst aan het concept, zeker in de landelijke gebieden, de kans om zich te zetten, om een zekere routine te worden. Evalueer de klachten, stuur bij als dat nodig is. En de allerlaatste stap is: als er een factuur aan vasthangt, zorg dan ook voor extra geld. Maar doe dat stapsgewijs, want als je dat geld meteen op tafel legt, dan is het weg, maar daarmee zijn de problemen nog niet opgelost. \n            ', '\n            Minister Lydia Peeters van de politieke partij Open Vld \n            heeft het volgende gezegd over  over de actuele situatie bij De Lijn: dat de verkiezingen daar wel iets mee te maken zullen hebben. (Opmerkingen van Stijn Bex) Er is veel veranderd met deze grote transitie. Routes veranderen, lijnnummers veranderen, haltes en reservatiesystemen veranderen. Hoppin is ingevoerd en er is de Mobiliteitscentrale. Ik hoor sommigen zeggen dat het allemaal niet werkt. Ik kan jullie het tegendeel bewijzen: het werkt wel. (Gelach bij Groen en Vooruit) We hebben hier meermaals verwijten gekregen dat het allemaal veel te lang duurt, dat ik het lef niet \n            ', '\n            Minister Lydia Peeters van de politieke partij Open Vld \n            heeft het volgende gezegd over  over de actuele situatie bij De Lijn: geven van de bijsturingen die we moeten doen, maar laat ons eerst doen wat we moeten doen: daar waar een gebrek of leemte is, zorgen we voor een bijsturing. Dat is de taak van De Lijn nu: continu monitoren en bijsturen en zorgen dat we vooruitgang boeken. Het is een goed plan, een plan waar heel veel reizigers wel bij varen en dat zien we aan de talrijke positieve reacties die we krijgen. \n            ', '\n            Mercedes Van Volcem (Open Vld) van de politieke partij Open Vld \n            heeft het volgende gezegd over  over de actuele situatie bij De Lijn: u al die goedkeuringen deed. (Applaus bij de meerderheid) Bovendien hebt u het over de kleine busjes. Ik vind de kleine busjes in de stad een megasucces, een ongelooflijk succes. Een mooi klein elektrisch busje waarvoor de hele Brugse gemeenteraad unaniem heeft gestreden en dat door de Brugse gemeenteraad ook werd goedgekeurd. Het stoort mij dat u hier onwaarheden poneert, tegen de feiten in. (Applaus bij de meerderheid) \n            ', '\n            Minister Lydia Peeters van de politieke partij Open Vld \n            heeft het volgende gezegd over  over de actuele situatie bij De Lijn: ze actievoeren. Dat vind ik larie en apekool. (Applaus bij de meerderheid) Ik blijf erbij ... De gemeenteraad van Sint-Truiden heeft dat plan goedgekeurd. De burgemeester van Wellen heeft dat plan goedgekeurd. (Opmerkingen van Ludwig Vandenhove en Steve Vandenberghe) Stop alstublieft met die onzin hier te verkondigen. Die plannen zijn goedgekeurd. Er zitten kinderziektes in, er zitten fouten in, en die sturen we bij. Te gepasten tijde wil ik u perfect de factuur geven van de bijsturingen die we moeten \n            ', '\n            Maurits Vande Reyde (Open Vld) van de politieke partij Open Vld \n            heeft het volgende gezegd over  over de herstructurering bij busbouwer Van Hool: moeten nemen, terwijl u enige tijd geleden in uw blaadje nog aankondigde dat u supertrots bent dat er drie weken stakingen was bij Van Hool. (Applaus bij Open Vld) Dat is het soort rechtsonzekerheid dat het vertrouwen van ondernemers ondermijnt. Collega’s, is er dan niks dat de Vlaamse overheid kan doen? Jawel, begeleiden naar jobs voor de rendabele onderdelen die er zijn bij Van Hool. Met name voor de touringcars en de truckafdeling kan er gekeken worden hoe een doorstart mogelijk is. Dat zal niet \n            ', '\n            Minister Lydia Peeters van de politieke partij Open Vld \n            heeft het volgende gezegd over  over de actuele situatie bij De Lijn: dus met te zeggen dat het niet kan. Mevrouw Lambrecht, ik heb de cijfers van De Lijn gekregen. In de drie dagen dat het up and running is, hebben 160 mensen met een beperking, een rollator of een rolstoel een boeking gedaan. Dat is hen gelukt. Zij kregen op hun aanvraag rolstoeltoegankelijk flexvervoer. Het systeem werkt dus wel degelijk. \n            '], 
                    "Groen": ["Tompie Tom zeg de situatie met de bussen van DeLijn is blablablabla"],
                    "cd&v": ["But Boemer zegt de situatie met de bussen van DeLijn DFSDFDF"],
                    }
                )
'''