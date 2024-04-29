import google.auth.transport.requests
import google.oauth2.id_token
import streamlit as st
import requests
import json
import os
import time
from streamlit_star_rating import st_star_rating
from PIL import Image

BACKEND_URL = "//"

# Take the path of current execution to find faction logos
execution_path = os.path.dirname(os.path.abspath(__file__))
logos_folder_path = "img"
full_path = os.path.join(execution_path,logos_folder_path)
print(full_path)
faction_logos = {filename.split(".")[0]: os.path.join(full_path, filename) for filename in os.listdir(logos_folder_path)}

# Load the images
#path_agents_img = os.path.join(execution_path,"img/debate.png")
#agents_img = Image.open(path_agents_img)

pvda_img = faction_logos['pvda']
groen_img = faction_logos['groen']
vooruit_img = faction_logos['vooruit']
cdv_img = faction_logos['cdv']
openvld_img = faction_logos['openvld']
nva_img = faction_logos['nva']
vlaamsbelang_img = faction_logos['vlaamsbelang']

if "generate" not in st.session_state:
    st.session_state.generate = False
if "json_content" not in st.session_state:
    st.session_state.json_content = ""
    
def small_text(text):
    return f"<span style='font-size: smaller'>{text}</span>"

def generate(query):
    try:
        auth_req = google.auth.transport.requests.Request()
        id_token = google.oauth2.id_token.fetch_id_token(auth_req, BACKEND_URL)
        print(auth_req.session.headers.values())
    
        
        # Include ID token in Authorization header
        headers = {"Authorization": f"Bearer {id_token}"}
        
        start_time = time.time()
        response = requests.post(f"{BACKEND_URL}/simulate", json={"query": query}, headers=headers)
        elapsed_time = time.time() - start_time
        #st.write(elapsed_time)
        
        if response.status_code == 200:
            st.session_state.json_content = response.content
            
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def send_review(stars, feedback, json_content):
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, BACKEND_URL)
    print(auth_req.session.headers.values())
    
    # Include ID token in Authorization header
    headers = {"Authorization": f"Bearer {id_token}"}
    response = requests.post(f"{BACKEND_URL}/review", json={"stars": stars, "feedback": feedback, "json_content": json_content}, headers=headers)

    print(response.status_code)

# Start the Streamlit frontend configuration
st.set_page_config(page_title='Politieke Copiloot', page_icon="🤖", initial_sidebar_state="auto", menu_items=None)

st.title("🤖 Welkom bij de Politieke Copiloot!")

st.write("Laat onze agents een virtueel politiek debat simuleren over een onderwerp naar keuze.")
#TODO: ADD loading bar/ spinner

with st.expander("Hoe werkt het?", expanded=False):
    st.write('''
            Heb je een politiek onderwerp waarover je graag een debat zou willen zien? Vul het onderwerp in en klik op de knop om het debat te simuleren.
            
            De AI Agents zullen relevante informatie verzamelen en onderling een virtueel debat simuleren.
            Elke politieke partij in Vlaanderen komt aan bod en heeft een eigen AI Agent die hun standpunten vertegenwoordigt.
            De data is afkomstig van de officiële partijprogramma's, de VRT en publieke uitspraken van functionarissen.
            Omdat het veel opzoekingswerk verricht kan het enige tijd duren voordat de resultaten worden weergegeven.
            
            Voorbeelden van onderwerpen: 
            
            "Er moeten meer buslijnen komen, ook op plaatsen waar weinig mensen opstappen."
            
            "Personeel van de Vlaamse overheid mag ⁠achter het loket⁠ een hoofddoek dragen."
            ''')
    
    #st.image(agents_img, use_column_width=True)

user_input = st.text_input(
    label="Geef een onderwerp voor het virtueel debat:",
    label_visibility="visible",
    placeholder="De schoolvakantie in de zomer moet ...",
    key="input",
    autocomplete="off"
)

 

simulate = st.button('Simuleer het debate')
st.markdown(small_text("_Pas op: dit is geen stemadvies._"), unsafe_allow_html=True)
#st.markdown(small_text("_Dit is slechts een experiment, blijf kritisch bij de output en kijk zeker de bronnen na._"), unsafe_allow_html=True)
                       

if simulate:
    if user_input == "":
        st.error("Geef eerst een onderwerp voor het virtueel debat")
    elif user_input != "":
        
        st.markdown("Het virtueel debat gaat van start! Net zoals echte politiekers pakken de agents hun tijd. Het generatieve proces kan tot twee minuten duren, even geduld...")
        generate(user_input)

         

if st.session_state.json_content:
    json_content = json.loads(st.session_state.json_content) 
               
    st.markdown("""---""")
    # Display the summary
    st.header("Samenvatting debat")
    st.write(json_content['summary'])
    st.markdown("""---""")
    # Display each faction's logo as a clickable block horizontally
    st.subheader("Standpunten")
    st.write("Gebruik de slider om de standpunten van een specifieke partij te lezen.")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    with col1:
        st.image(pvda_img, use_column_width=True)
            
    with col2:
        st.image(groen_img, use_column_width=True)

    with col3:
        st.image(vooruit_img, use_column_width=True)
            
    with col4:
        st.image(cdv_img, use_column_width=True)
            
    with col5:
        st.image(openvld_img, use_column_width=True)

    with col6:
        st.image(nva_img, use_column_width=True)

    with col7:
        st.image(vlaamsbelang_img, use_column_width=True)

    list = ['pvda', 'groen', 'vooruit', 'cdv', 'openvld', 'nva', 'vlaamsbelang']
        
    slider_value = st.select_slider(label="Kies een partij van Links tot Rechts", options=list,label_visibility="hidden")

    st.subheader(f"Het standpunt van {slider_value.capitalize()}:")
    st.write(json_content[slider_value])
    
    st.markdown("""---""")
    
    
    # Add relevancy rating feature
    #stars = st_star_rating(label="Beoordeel de relevantie van de inhoud", 
    #                        maxValue=5, 
    #                    defaultValue=None, 
    #                    size=50, emoticons=True, 
    #                    read_only=False, 
    #                    dark_theme=False, 
    #                    resetButton=False, 
    #                    resetLabel="Reset Rating",
    #                    customCSS="")

    stars = st.slider("Beoordeel de relevantie van de inhoud:", 1, 5, 3)
    feedback = st.text_area("Wij zijn benieuwd naar jouw mening!", placeholder="...")
    
    if stars is not None:
        if st.button("Verzend", on_click=send_review(stars, feedback, json_content)):
            st.write("Bedankt voor jouw feedback!")
          
st.write("---")
st.markdown(small_text("Disclaimer: deze applicatie is slechts een demo van AI multi-Agents. Het kan fouten bevatten en is nog in ontwikkeling. Het is niet de bedoeling om kiezers te beïnvloeden maar hen slechts wegwijs te maken in de overvloed aan data. Feedback is welkom: cascoopman@hotmail.com"),unsafe_allow_html=True)

# Optional code to ask the user for their OpenAI API key
# if you just want to use the .env file, uncomment the following lines
#from decouple import config
#if config('OPENAI_API_KEY', default=None) is not None:
#    os.environ["OPENAI_API_KEY"] = config('OPENAI_API_KEY')

# Optional code to include a background image
page_element="""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://images.unsplash.com/photo-1604147706283-d7119b5b822c?q=80&w=2187&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
  background-size: cover;
  background-position: left bottom;
}
</style>
"""

#st.markdown(page_element, unsafe_allow_html=True)