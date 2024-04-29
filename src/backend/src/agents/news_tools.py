import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin 
import os
import json
from openai import OpenAI

def get_suburls(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract all anchor tags (links) from the page
            links = soup.find_all('a')
            
            # Extract the base URL
            base_url = urlparse(url).scheme + '://' + urlparse(url).netloc
            
            # List to store suburls
            suburls = []
            
            # Loop through all links and extract suburls
            for link in links:
                href = link.get('href')
                if href and not href.startswith('#'):
                    # Join the base URL with the extracted href to get the absolute URL
                    absolute_url = urljoin(base_url, href)
                    suburls.append(absolute_url)
            
            return suburls
        else:
            print("Failed to fetch URL:", url)
            return []
    except Exception as e:
        print("An error occurred:", str(e))
        return []

def get_content(url):
    # Send a GET request to the URL
    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Find the div element with the specified class
            div_element = soup.find_all("div", class_="text")
            
            extracted_text = ""
            # Extract and print the text if the element is found
            if div_element:
                for div in div_element:
                    extracted_text += div.get_text(separator="\n")
                extracted_text += "[Bron: " + url + "]"
                extracted_text = extracted_text.replace('\n', '')
                extracted_text = extracted_text.replace('\xa0', '')
                print(repr(extracted_text))
                return extracted_text
            else:
                print("Div element not found.")
                return "No content found."
        else:
            print("Failed to retrieve the webpage.")
            return "No content found."
    except Exception as e:
        print("An error occurred:", str(e))
        return "No content found."

def get_news_domestic_politics(topic, topK = 3) -> list[str]:
    # Example usage:
    url = "https://www.vrt.be/vrtnws/nl/net-binnen/kies24/"  # Replace with your desired URL
    suburls = get_suburls(url)

    try: suburls.remove(url)
    except: pass
    
    print(suburls)
    
    # Get OpenAI API key
    current_directory = os.path.dirname(__file__)
    absolute_path = os.path.abspath(os.path.join(current_directory, "OAI_CONFIG_LIST.json"))
    with open(absolute_path, "r") as file:
        config_list = json.load(file)
    
    # Send the URL to openAI
    # TODO: Change faction
    openAI = OpenAI(api_key=config_list[0]["api_key"])
    completion = create_completion(openAI, topic, suburls, topK)

    # open the chat completions
    print(repr(completion.choices[0].message.content))
    
    links_string = completion.choices[0].message.content

    # Split the string based on newline character to get individual links
    links_list = links_string.split('\n')

    print(links_list)
    chunks = []
    for link in links_list:
        chunks.append(get_content(link))
    
    return chunks

def create_completion(openAI, topic, filtered_sub_urls, topK):
    return openAI.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.0,
        messages=[
            {"role": "system", "content": f'''
                Je kiest de suburls uit een lijst van URLs die informatie.
                De website is een nieuwswebsite over politiek in België, Vlaanderen.
                Het is jouw taak om de meeste toepasselijke suburls te kiezen voor het onderwerp {topic}.
                Geef enkel een bestaande URL
                
                Welke pagina zal de meeste relevante informatie bevatten voor het onderwerp?
                
                Jij antwoordt enkel met de URLs die gegeven zijn. 
                Gebruik geen nummering of opsommingstekens.
                Per lijn één URL.
                
                Geef de top {topK} suburls die informatie bevatten voor het onderwerp: {topic}.
                Kies de suburls die het meest relevante zijn voor het onderwerp.
                
                Hieronder de lijst van suburls die je kan gebruiken.
                Indien geen relevant URL gevonden, antwoord met "Geen relevante URL gevonden".
                Verzin zelf geen url, geef de volledige URL en voeg geen tekens toe.
                Haal hieruit de meest relevante suburls voor het onderwerp {topic}:
                {filtered_sub_urls}
                '''
                }
            ]
        )

if __name__ == "__main__":
    print(get_news_domestic_politics(topic="Abortus moet niet toegelaten zijn", topK=3))