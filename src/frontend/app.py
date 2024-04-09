import os
import streamlit as st
#from agents.manual_debate import run_manual_debate

st.set_page_config(page_title='AI Agent', page_icon='🧙🏻‍♂️', initial_sidebar_state="auto", menu_items=None)
st.title("Political Debate Simulator 🤖")

# if you just want to use the .env file, uncomment the following lines
#from decouple import config
#if config('OPENAI_API_KEY', default=None) is not None:
#    os.environ["OPENAI_API_KEY"] = config('OPENAI_API_KEY')

st.sidebar.title("Enter Your API Key 🗝️")
open_api_key = st.sidebar.text_input(
    "Open API Key", 
    value=st.session_state.get('open_api_key', ''),
    help="Get your API key from https://openai.com/",
    type='password'
)
os.environ["OPENAI_API_KEY"] = open_api_key


st.session_state['open_api_key'] = open_api_key

user_input = st.text_input(
    "State a topic for the virtual debate below, and let our AI agents help you make an informed decision.", 
    placeholder="I am in favor of universal basic income because ...",
    key="input"
)


if st.button('Simulate Debate'):
    #if user_input != "" and (open_api_key == ''):
    #    st.error("Please enter your API keys in the sidebar")
    if user_input == "":
        st.error("Please enter a topic for the debate")
    elif user_input != "":
        st.info("Running the debate simulation...")
        
        
        #run_manual_debate(
        #    user_input=user_input,
        #    num_iterations=num_iterations,
        #    baby_agi_model=baby_agi_model,
        #    todo_chaining_model=todo_chaining_model,
        #    embedding_model=embedding_model,
            # embedding_size=embedding_size
        #)

with st.expander(label="Advanced Settings", expanded=False):
    include_all = st.checkbox('Include all Factions', value=True)
    
    if include_all:
        st.write('All factions are participating in the debate!')
    else:
        st.write("---")
        included_parties = []
        columns = st.columns(3)  # Divide the expander into two columns
        
        with columns[0]:
            groen = st.checkbox('Groen')
            if groen:
                included_parties.append("Groen")

            nva = st.checkbox('NVA')
            if nva:
                included_parties.append("NVA")

            cdv = st.checkbox('cd&v')
            if cdv:
                included_parties.append("cd&v")

        with columns[1]:
            vooruit = st.checkbox('Vooruit')
            if vooruit:
                included_parties.append("Vooruit")

            vlaams_belang = st.checkbox('Vlaams Belang')
            if vlaams_belang:
                included_parties.append("Vlaams Belang")

            pvda = st.checkbox('PVDA')
            if pvda:
                included_parties.append("PVDA")
 
        with columns[2]:
            openvld = st.checkbox('Open VLD')
            if openvld:
                included_parties.append("Open VLD")

        if len(included_parties) == 0:
            st.write("No factions selected!")
        else:
            st.write("The following Faction(s) are participating in the debate:")
            st.write(f"{included_parties}")