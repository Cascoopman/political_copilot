import google.auth.transport.requests
import google.oauth2.id_token
import streamlit as st
import requests
import json

BACKEND_URL = "//"

def backend(query):
    try:
        auth_req = google.auth.transport.requests.Request()
        id_token = google.oauth2.id_token.fetch_id_token(auth_req, BACKEND_URL)
        print(auth_req.session.headers.values())
        
        # Include ID token in Authorization header
        headers = {"Authorization": f"Bearer {id_token}"}
        response = requests.post(f"{BACKEND_URL}/simulate", json={"query": query}, headers=headers)
        
        if response.status_code == 200:
            json_content = json.loads(response.content)
                        
            # Display the summary
            st.header("Samenvatting debat 🤓")
            st.write(json_content['summary'])
            
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

#TODO: add transparantie (AI-Act)
st.set_page_config(page_title='Politieke Copiloot', page_icon='‍♂️', initial_sidebar_state="auto", menu_items=None)
st.title("Politiek debat simulator ")

user_input = st.text_input(
    "Geef hieronder een onderwerp op voor het virtuele debat en laat onze AI-agenten je helpen om een weloverwogen beslissing te nemen.", 
    placeholder="Ik ben voorstander van een universeel basisinkomen omdat ...",
    key="input",
    autocomplete="off"
)

if st.button('Simuleer het debate'):
    if user_input == "":
        st.error("Geef eerst een onderwerp voor het virtueel debat")
    elif user_input != "":
        st.info("Het virtueel debat wordt in gang gezet...")
        results = backend(user_input)

# if you just want to use the .env file, uncomment the following lines
#from decouple import config
#if config('OPENAI_API_KEY', default=None) is not None:
#    os.environ["OPENAI_API_KEY"] = config('OPENAI_API_KEY')



#st.sidebar.title("Enter Your API Key 🗝️")
#open_api_key = st.sidebar.text_input(
#    "Open API Key", 
#    value=st.session_state.get('open_api_key', ''),
#    help="Get your API key from https://openai.com/",
#    type='password'
#)
#os.environ["OPENAI_API_KEY"] = open_api_key
#st.session_state['open_api_key'] = open_api_key

#with st.expander(label="Advanced Settings", expanded=False):
#    include_all = st.checkbox('Include all Factions', value=True)
#    
#    if include_all:
#        st.write('All factions are participating in the debate!')
#    else:
#        st.write("---")
#        included_parties = []
#        columns = st.columns(3)  # Divide the expander into two columns
#        
#        with columns[0]:
#            groen = st.checkbox('Groen')
#            if groen:
#                included_parties.append("Groen")
#
#            nva = st.checkbox('NVA')
#            if nva:
#                included_parties.append("NVA")
#
#            cdv = st.checkbox('cd&v')
#            if cdv:
#                included_parties.append("cd&v")
#
#        with columns[1]:
#            vooruit = st.checkbox('Vooruit')
#            if vooruit:
#                included_parties.append("Vooruit")
#
#            vlaams_belang = st.checkbox('Vlaams Belang')
#            if vlaams_belang:
#                included_parties.append("Vlaams Belang")
#
#            pvda = st.checkbox('PVDA')
#            if pvda:
#                included_parties.append("PVDA")
# 
#        with columns[2]:
#            openvld = st.checkbox('Open VLD')
#            if openvld:
#                included_parties.append("Open VLD")
#
#        if len(included_parties) == 0:
#            st.write("No factions selected!")
#        else:
#            st.write("The following Faction(s) are participating in the debate:")
#            st.write(f"{included_parties}")