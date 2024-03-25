import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
import html2text

import logging

def remove_html_tags(input_html):
    # Convert HTML to plain text
    text = html2text.html2text(input_html)
    
    return text

def extract_main_content(html):
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find the main element with id="content"
    main_content_element = soup.find('main', id='content')

    # Check if the main_content_element exists
    if main_content_element:
        # Extract the plain text from the main content element
        plain_text_content = remove_html_tags(
            main_content_element.get_text(separator='\n', strip=True)
        )
        return plain_text_content
    else:
        return ""


class VooruitSpider(CrawlSpider):
    name = 'vooruit'
    # allowed_domains = ['vooruit.org']
    start_urls = ['https://www.vooruit.org']

    rules = (
        Rule(LinkExtractor(allow=(r'^https?://(?:\w+\.)?vooruit\.org'), allow_domains="vooruit.org"),
            callback='parse_page', follow=True
        ),
        Rule(LinkExtractor(allow=('\.pdf')), callback='parse_pdf', follow=False),
    )

    visited_pages = dict()

    def parse_page(self, response):
        url = response.url
        body = bytes(extract_main_content(response.text), 'utf-8').decode('unicode-escape').encode('latin-1').decode('utf-8')

        if url not in self.visited_pages:
            logging.info(f'PAGE: {url}')
            self.visited_pages[url] = body
            yield {
                'url': url,
                'body': body,
            }
            
    def parse_pdf(self, response):
        url = response.url
        logging.info(f'PDF: {url}')
        yield {
                'url': url,
                'body': "EXTRACT INFO FROM PDF",
            }
