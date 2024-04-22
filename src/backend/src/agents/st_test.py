import streamlit as st
from streamlit_star_rating import st_star_rating
import json
import os
import time
import random

# Assuming json_content is your loaded JSON data
json_content = {
    'summary': "Summary of the debate",
    'coalition': "Expected coalition",
    'pvda': "Viewpoint of Faction A",
    'groen': "Viewpoint of Faction B",
    'vooruit': "Viewpoint of Faction C"
}

# Take the path of current execution
execution_path = os.path.dirname(os.path.abspath(__file__))
logos_folder_path = "/Users/cas/Documents/political_agents/src/backend/src/agents/img"
full_path = os.path.join(execution_path,logos_folder_path)
print(full_path)

faction_logos = {filename.split(".")[0]: os.path.join(full_path, filename) for filename in os.listdir(logos_folder_path)}

loop = 0

if st.button('Simuleer het debat'):
    query = 'Moeten we kernenergie behouden?'
    st.write(f'Het onderwerp van dit debat: {query}')
    time.sleep(random.randint(2, 3))
    st.session_state.text = st.session_state.get('text', 'Het onderwerp is verzonden! \n')
    logtxtbox = st.empty()
    logtxtbox.text_area("Vooruitgang simulatie: ",st.session_state.text, height = 50)
    time.sleep(random.randint(4, 7))
    
    st.session_state.text += 'De vertegenwoordigers worden aangeduid. \n' 
    logtxtbox.text_area("Vooruitgang simulatie: ",st.session_state.text, height = 50)
    time.sleep(random.randint(4, 7))
    
    st.session_state.text += 'De sprekers maken zich gereed om te debatteren. \n' 
    logtxtbox.text_area("Vooruitgang simulatie: ",st.session_state.text, height = 50)
    time.sleep(random.randint(4, 7))
    
    st.session_state.text += 'Het virtueel debat is van start gegaan! \n' 
    logtxtbox.text_area("Vooruitgang simulatie: ",st.session_state.text, height = 50)
    time.sleep(random.randint(4, 7))
    
    st.session_state.text += 'Elke partij komt nu aan de beurt en jij krijgt de samenvatting. \n' 
    logtxtbox.text_area("Vooruitgang simulatie: ",st.session_state.text, height = 50)
    time.sleep(random.randint(3, 6))
    
    st.session_state.text += 'Er wordt hevig gediscussieerd. \n' 
    logtxtbox.text_area("Vooruitgang simulatie: ",st.session_state.text, height = 50)
    time.sleep(random.randint(8, 12))
    
    st.session_state.text += 'Het debat is bijna afgelopen... \n' 
    logtxtbox.text_area("Vooruitgang simulatie: ",st.session_state.text, height = 50)
    time.sleep(random.randint(8, 12))
    
    loop = 1
    
if loop == 1:    
    # Display the summary
    st.header("Samenvatting debat")
    st.write(json_content['summary'])

    screen = st.empty()

    # Display each faction's logo as a clickable block horizontally
    st.subheader("Standpunten")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    if 'button_pvda_pressed' not in st.session_state:
            st.session_state.button_pvda_pressed = False

    selected_viewpoint = None

    with col1:
        st.image(faction_logos['pvda'], use_column_width=True)
        if st.button('PVDA'):
            selected_viewpoint = 'pvda'
            
    with col2:
        st.image(faction_logos['groen'], use_column_width=True)
        if st.button('Groen'):
            selected_viewpoint = 'groen'

    with col3:
        st.image(faction_logos['vooruit'], use_column_width=True)
        if st.button('Vooruit'):
            selected_viewpoint = 'vooruit'
            
    with col4:
        st.image(faction_logos['cdv'], use_column_width=True)
        if st.button('cd&v'):
            selected_viewpoint = 'cdv'
            
    with col5:
        st.image(faction_logos['openvld'], use_column_width=True)
        if st.button('openvld'):
            selected_viewpoint = 'openvld'
            
    with col6:
        st.image(faction_logos['nva'], use_column_width=True)
        if st.button('nva'):
            selected_viewpoint = 'nva'

    with col7:
        st.image(faction_logos['vlaamsbelang'], use_column_width=True)
        if st.button('vlaamsbelang'):
            selected_viewpoint = 'vlaamsbelang'
            
    if selected_viewpoint:
        st.write(json_content[selected_viewpoint])

    stars=None
        
    # Add relevancy rating feature
    stars = st_star_rating(label="Beoordeel de relevantie van de inhoud", 
                            maxValue=5, 
                        defaultValue=None, 
                        size=50, emoticons=True, 
                        read_only=False, 
                        dark_theme=False, 
                        resetButton=False, 
                        resetLabel="Reset Rating",
                        customCSS="", on_click=None)

    feedback = st.text_area("Wij zijn benieuwd naar jouw mening!", placeholder="...")

    def send_review(value):
        # Send the review to the backend
        pass

    if stars is not None:
        if st.button("Verzend", on_click=send_review(stars)):
            st.write("Bedankt voor jouw feedback!")


    # Display the coalition expectations
    with st.expander("Coalitie verwachtingen 🤝"):
        st.write(json_content['coalition'])
        