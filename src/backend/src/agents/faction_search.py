import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from openai import OpenAI
import os
import json

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

def get_content_pvda(url):
    # Send a GET request to the URL
    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Find the div element with the specified class
            div_element = soup.find("div", class_="hero__intro text")
            
            # Extract and print the text if the element is found
            if div_element:
                extracted_text = div_element.get_text(separator="\n")
                extracted_text = "Op de website van de PVDA staat:" + extracted_text + "[Bron: " + url + "]"
                print(extracted_text)
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

def tool_pvda(topic, topK = 15) -> list[str]:
    # Example usage:
    url = "https://www.pvda.be/programma"  # Replace with your desired URL
    suburls = get_suburls(url)

    # Filter the URLs
    filtered_sub_urls = [link for link in suburls if link.startswith(f"{url}/")]

    print(filtered_sub_urls)
    
    # Get OpenAI API key
    current_directory = os.path.dirname(__file__)
    absolute_path = os.path.abspath(os.path.join(current_directory, "OAI_CONFIG_LIST.json"))
    with open(absolute_path, "r") as file:
        config_list = json.load(file)
    
    # Send the URL to openAI
    openAI = OpenAI(api_key=config_list[0]["api_key"])
    completion = create_completion(openAI, topic, filtered_sub_urls, topK, faction="PVDA")

    # open the chat completions
    print(repr(completion.choices[0].message.content))
    
    links_string = completion.choices[0].message.content

    # Split the string based on newline character to get individual links
    links_list = links_string.split('\n')

    print(links_list)
    chunks = []
    for link in links_list:
        chunks.append(get_content_pvda(link))
    
    return chunks

def get_content_groen(url):
        # Send a GET request to the URL
    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Find the div element with the specified class
            div_element = soup.find_all("div", class_="col-md-10")
            
            # Extract and print the text if the element is found
            if len(div_element) >= 1:
                extracted_text = div_element[1].get_text(separator="\n")
                extracted_text = "Op de website van Groen staat:" + extracted_text + "[Bron: " + url + "]"
                print(extracted_text)
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

def tool_groen(topic, topK = 8) -> list[str]:
    # Example usage:
    url = "https://www.groen.be/standpunten"  # Replace with your desired URL
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
    openAI = OpenAI(api_key=config_list[0]["api_key"])
    completion = create_completion(openAI, topic, suburls, topK, faction="Groen")

    # open the chat completions
    print(repr(completion.choices[0].message.content))
    
    links_string = completion.choices[0].message.content

    # Split the string based on newline character to get individual links
    links_list = links_string.split('\n')

    print(links_list)
    chunks = []
    for link in links_list:
        chunks.append(get_content_groen(link))
    
    return chunks

def get_content_vooruit(url):
        # Send a GET request to the URL
    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Find the div element with the specified class
            div_element = soup.find("div", class_="pov-page__content")
            
            # Extract and print the text if the element is found
            if div_element:
                extracted_text = div_element.get_text(separator="\n")
                extracted_text = "Op de website van Vooruit staat:" + extracted_text + "[Bron: " + url + "]"
                print(extracted_text)
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

def tool_vooruit(topic, topK = 3) -> list[str]:
    # Example usage:
    url = "https://www.vooruit.org/standpunten"  # Replace with your desired URL
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
    completion = create_completion(openAI, topic, suburls, topK, faction="Vooruit")

    # open the chat completions
    print(repr(completion.choices[0].message.content))
    
    links_string = completion.choices[0].message.content

    # Split the string based on newline character to get individual links
    links_list = links_string.split('\n')

    print(links_list)
    chunks = []
    for link in links_list:
        chunks.append(get_content_vooruit(link))
    
    return chunks

def get_content_cdv(url):
        # Send a GET request to the URL
    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Find the div element with the specified class
            div_element = soup.find("div", class_="col")
            
            # Extract and print the text if the element is found
            if div_element:
                extracted_text = div_element.get_text(separator="\n")
                extracted_text = "Op de website van cd&v staat:" + extracted_text + "[Bron: " + url + "]"
                print(extracted_text)
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

def tool_cdv(topic, topK = 5) -> list[str]:
    # Example usage:
    url = "https://www.cdenv.be/onze_standpunten"  # Replace with your desired URL
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
    completion = create_completion(openAI, topic, suburls, topK, faction="cd&v")

    # open the chat completions
    print(repr(completion.choices[0].message.content))
    
    links_string = completion.choices[0].message.content

    # Split the string based on newline character to get individual links
    links_list = links_string.split('\n')

    print(links_list)
    chunks = []
    for link in links_list:
        chunks.append(get_content_cdv(link))
    
    return chunks

def get_content_openvld(url):
        # Send a GET request to the URL
    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Find the div element with the specified class
            div_element = soup.find("div", class_="col-lg-8")
            
            # Extract and print the text if the element is found
            if div_element:
                extracted_text = div_element.get_text(separator="\n")
                extracted_text = "Op de website van Open Vld staat:" + extracted_text + "[Bron: " + url + "]"
                print(extracted_text)
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

def tool_openvld(topic, topK = 3) -> list[str]:
    # Example usage:
    url = "https://www.openvld.be/standpunten"  # Replace with your desired URL
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
    completion = create_completion(openAI, topic, suburls, topK, faction="Open Vld")

    # open the chat completions
    print(repr(completion.choices[0].message.content))
    
    links_string = completion.choices[0].message.content

    # Split the string based on newline character to get individual links
    links_list = links_string.split('\n')

    print(links_list)
    chunks = []
    for link in links_list:
        chunks.append(get_content_openvld(link))
    
    return chunks

def get_content_nva(url):
    # Send a GET request to the URL
    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Find the div element with the specified class
            div_element = soup.find("div", class_="term--topics--full taxonomy-term vocabulary-topics")
            
            # Extract and print the text if the element is found
            if div_element:
                extracted_text = div_element.get_text(separator="\n")
                extracted_text = "Op de website van N-VA staat:" + extracted_text + "[Bron: " + url + "]"
                print(extracted_text)
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

def tool_nva(topic, topK = 6) -> list[str]:
        # Example usage:
    url = "https://www.n-va.be/standpunten"  # Replace with your desired URL
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
    completion = create_completion(openAI, topic, suburls, topK, faction="N-VA")

    # open the chat completions
    print(repr(completion.choices[0].message.content))
    
    links_string = completion.choices[0].message.content

    # Split the string based on newline character to get individual links
    links_list = links_string.split('\n')

    print(links_list)
    chunks = []
    for link in links_list:
        chunks.append(get_content_nva(link))
    
    return chunks

def get_content_vlaamsbelang(url):
    # Send a GET request to the URL
    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Find the div element with the specified class
            div_element = soup.find("div", class_="p-text__content")
            
            # Extract and print the text if the element is found
            if div_element:
                extracted_text = div_element.get_text(separator="\n")
                extracted_text = "Op de website van Vlaams Belang staat:" + extracted_text + "[Bron: " + url + "]"
                print(extracted_text)
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

def tool_vlaamsbelang(topic, topK = 6) -> list[str]:
    # Example usage:
    url = "https://www.vlaamsbelang.org/programma"  # Replace with your desired URL
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
    completion = create_completion(openAI, topic, suburls, topK, faction="Vlaams Belang")

    # open the chat completions
    print(repr(completion.choices[0].message.content))
    
    links_string = completion.choices[0].message.content

    # Split the string based on newline character to get individual links
    links_list = links_string.split('\n')

    print(links_list)
    chunks = []
    for link in links_list:
        chunks.append(get_content_vlaamsbelang(link))
    
    return chunks

def create_completion(openAI, topic, filtered_sub_urls, topK, faction):
    return openAI.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.0,
        messages=[
            {"role": "system", "content": f'''
                Je kiest de suburls uit een lijst van URLs die informatie.
                Het is de website van de politieke partij {faction}.
                Het is jouw taak om de meeste toepasselijke suburls te kiezen voor het onderwerp {topic}.
                Geef enkel een bestaande URL
                Welke pagina zal de meeste relevante informatie bevatten voor het onderwerp?
                
                Jij antwoordt enkel met de URLs die gegeven zijn. 
                Gebruik geen nummering of opsommingstekens.
                Per lijn één URL.
                
                Geef de top {topK} suburls die informatie bevatten voor het onderwerp: {topic}.
                Kies de suburls die het meest relevante zijn voor het onderwerp.
                
                Hieronder de lijst van suburls die je kan gebruiken.
                Verzin zelf geen url, geef de volledige URL en voeg geen tekens toe.
                Haal hieruit de meest relevante suburls voor het onderwerp {topic}:
                {filtered_sub_urls}
                '''
                }
            ]
        )

def faction_search(topic, faction) -> list[str]:
    tools = {
        "PVDA": tool_pvda, # Werkt
        "Groen": tool_groen, # Werkt
        "Vooruit": tool_vooruit, # Werkt
        "cd&v": tool_cdv, # Werkt
        "Open Vld": tool_openvld, # Werkt
        "N-VA": tool_nva, # Werkt
        "Vlaams Belang": tool_vlaamsbelang # Werkt
    }
    return tools[faction](topic)
      
if __name__ == "__main__":
    # For testing purposes
    #print(get_suburls("https://www.vrt.be/vrtnws/nl/kies24/vlaams_parlement/"))
    filtered_sub_urls = get_suburls("https://www.vrt.be/vrtnws/nl/2024/03/25/vlaams-belang-waar-staat-de-partij-voor/")
    print(filtered_sub_urls)
    quit()

    openAI = OpenAI()
    topic = "klimaat"
    topK = 5
    response = openAI.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.0,
        messages=[
            {"role": "system", "content": f'''
                Je kiest de suburls uit een lijst van URLs die informatie.
                Het is een nieuws website.
                Het is jouw taak om de meeste toepasselijke suburls te kiezen voor het onderwerp {topic}.
                Geef enkel een bestaande URL.
                Indien geen relevant URL, stuur een lege string.
                
                Welke pagina zal de meeste relevante informatie bevatten voor het onderwerp?
                
                Jij antwoordt enkel met de URLs die gegeven zijn. 
                Gebruik geen nummering of opsommingstekens.
                Per lijn één URL.
                
                Geef de top {topK} suburls die informatie bevatten voor het onderwerp: {topic}.
                Kies de suburls die het meest relevante zijn voor het onderwerp.
                
                Hieronder de lijst van suburls die je kan gebruiken.
                Verzin zelf geen url, geef de volledige URL en voeg geen tekens toe.
                Haal hieruit de meest relevante suburls voor het onderwerp {topic}:
                {filtered_sub_urls}
                '''
                }
            ]
        )
    print(repr(response.choices[0].message.content))