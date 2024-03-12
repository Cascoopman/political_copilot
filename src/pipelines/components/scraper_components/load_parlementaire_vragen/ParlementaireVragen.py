import requests
from bs4 import BeautifulSoup
import os
import shutil
import re


def run():
    THEMA = "natuur_en_milieu"
    THEMA_QUERY = "Natuur en Milieu"
    CURRENT_YEAR_OF_OFFICE_VALUE = "2022-2023"
    AMOUNT_OF_PAGES = 1 # Here I manually found from the search engine that there are 12 pages on the URL
    
    for page_number in range(0,AMOUNT_OF_PAGES): 
        request_URL = f"https://www.vlaamsparlement.be/ajax/document-overview?page={page_number}&period=current_year_of_office&current_year_of_office_value=2022-2023&aggregaat%5B%5D=Vraag%20of%20interpellatie&aggregaattype%5B%5D=Schriftelijke%20vraag&thema%5B%5D=Natuur%20en%20Milieu"
        #request_URL = f"https://www.vlaamsparlement.be/ajax/document-overview?page={page_number}&period=current_year_of_office&current_year_of_office_value={CURRENT_YEAR_OF_OFFICE_VALUE}&aggregaat%5B%5D=Vraag%20of%20interpellatie&aggregaattype%5B%5D=Schriftelijke%20vraag&thema%5B%5D={THEMA_QUERY}"
        #request_URL = CUSTOM_LINK
        headers = {'Accept': 'application/json'}
        response = requests.get(request_URL, headers=headers)

        json_content = response.json()
        html_content = json_content['html']

        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all articles with class "card card--document"
        articles = soup.find_all('article', class_='card card--document')
        i = 0
        # Loop through each article
        for article in articles:
            i += 1 
            # Extract the card title
            card_title = article.find('h3', class_='card__title').get_text()
            
            # Extract the document number
            doc_number = article.find('span', class_='card__document-number').get_text()
            
            # Find the link with class "card__link card__link-view"
            view_link = article.find('li', class_='card__link card__link-view')
            # Find the link with class "card__link card__link-download"
            download_link = article.find('li', class_='card__link card__link-download')
            
            # Extract the text and href attribute from the view link, if it exists        
            if view_link:
                view_text = view_link.get_text()
                view_href = view_link.find('a')['href']
            else:
                view_text, view_href = '', ''
            
            # Extract the text and href attribute from the download link, if it exists
            if download_link:
                download_text = download_link.get_text()
                download_href = download_link.find('a')['href']
            else:
                download_text, download_href = '', ''
            
            # Print the extracted information
            print('Card title:', card_title)
            print('Document number:', doc_number)
            print('View link text:', view_text)
            print('View link href:', view_href)
            print('Download link text:', download_text)
            print('Download link href:', download_href)

            card_title = card_title.replace("/", "_") #otherwise it will try to find a folder
            file_name = f"{card_title}_{doc_number}"

            # Download the pdf and save it to a file
            pdf_url = download_href
            response = requests.get(pdf_url)
            os.makedirs(os.path.dirname(f"/microservice/app/scrapers/output_pdfs/{THEMA}/{file_name}.pdf"), exist_ok=True)
            with open(f"/microservice/app/scrapers/output_pdfs/{THEMA}/{file_name}.pdf", "wb") as file:
                file.write(response.content)

            print(f"Downloaded {file_name}.pdf")
            print(f"Handeled Page {page_number} Article # {i}")

def name_change():            
    folder_path = "/Users/cas/Downloads/output_pdfs/natuur_en_milieu/"

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pdf'):
            new_file_name = file_name.replace(' ', '_')
            while not re.match(r'^[a-zA-Z]', new_file_name):
                new_file_name = new_file_name[1:]
            if new_file_name != file_name:
                os.rename(os.path.join(folder_path, file_name), os.path.join(folder_path, new_file_name))
                print(f"Renamed file {file_name} to {new_file_name}")

if __name__ == "__main__":
    name_change()