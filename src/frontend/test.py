import streamlit as st
from streamlit_star_rating import st_star_rating
import json
import os
import time
import random

# Assuming json_content is your loaded JSON data


# Take the path of current execution
execution_path = os.path.dirname(os.path.abspath(__file__))
logos_folder_path = "/Users/cas/Documents/political_agents/src/frontend/img"
full_path = os.path.join(execution_path,logos_folder_path)
print(full_path)

faction_logos = {filename.split(".")[0]: os.path.join(full_path, filename) for filename in os.listdir(logos_folder_path)}


def generate():
    st.session_state.generate = True
    st.session_state.json_content = {
    'summary': "Summary of the debate",
    'coalition': "Expected coalition",
    'pvda': "Viewpoint of Faction A",
    'groen': "Viewpoint of Faction B",
    'vooruit': "Viewpoint of Faction C",
    'cdv': "Viewpoint of Faction D",
    'openvld': "Viewpoint of Faction E",
    'nva': "Viewpoint of Faction F",
    'vlaamsbelang': "Viewpoint of Faction G"
    }
    time.sleep(random.randint(1, 5))
    st.session_state.test = "test"
       

if "generate" not in st.session_state:
    st.session_state.generate = False
if "test" not in st.session_state:
    st.session_state.test = ""
if "json_content" not in st.session_state:
    st.session_state.json_content = ""
if "selected_viewpoint" not in st.session_state:
    st.session_state.selected_viewpoint = "cdv"

st.set_page_config(page_title="Test", page_icon="🤖")
st.title("Politiek debat simulator ")

if st.button('Simuleer het debat'):
    generate()
    

if st.session_state.test:
    st.markdown("""---""")
    # Display the summary
    st.header("Samenvatting debat")
    st.write(st.session_state.json_content['summary'])

    # Display each faction's logo as a clickable block horizontally
    st.subheader("Standpunten")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    with col1:
        st.image(faction_logos['pvda'], use_column_width=True)
            
    with col2:
        st.image(faction_logos['groen'], use_column_width=True)

    with col3:
        st.image(faction_logos['vooruit'], use_column_width=True)
            
    with col4:
        st.image(faction_logos['cdv'], use_column_width=True)
            
    with col5:
        st.image(faction_logos['openvld'], use_column_width=True)

    with col6:
        st.image(faction_logos['nva'], use_column_width=True)

    with col7:
        st.image(faction_logos['vlaamsbelang'], use_column_width=True)

    list = ['pvda', 'groen', 'vooruit', 'cdv', 'openvld', 'nva', 'vlaamsbelang']
        
    slider_value = st.select_slider(label="Kies een partij van Links tot Rechts", options=list,label_visibility="hidden")

    st.write(st.session_state.json_content[slider_value])
    
    st.markdown("""---""")
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

    st.markdown("""---""")
    # Display the coalition expectations
    with st.expander("Coalitie verwachtingen 🤝"):
        st.write(st.session_state.json_content['coalition'])