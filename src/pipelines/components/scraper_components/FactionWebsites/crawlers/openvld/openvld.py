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
    main_content_element = soup.find('div', id='middle')

    # for nav_element in soup.find_all('nav', class_='breadcrumb'):
    #     nav_element.decompose()

    # for aside_element in soup.find_all('aside', class_='sidebar'):
    #     aside_element.decompose()

    # for div_element in soup.find_all('div', class_='page-layout__footer'):
    #     div_element.decompose()

    # Check if the main_content_element exists
    if main_content_element:
        # Extract the plain text from the main content element
        plain_text_content = remove_html_tags(
            main_content_element.get_text(separator='\n', strip=True)
        )
        return plain_text_content
    else:
        # Extract the plain text from the entire web page
        plain_text_content = remove_html_tags(
            soup.get_text(separator='\n', strip=True)
        )
        return plain_text_content

class OpenVldSpider(CrawlSpider):
    name = 'openvld'
    start_urls = ['https://www.openvld.be/']

    rules = (
        Rule(LinkExtractor(allow=(r'^https?://(?:\w+\.)?openvld\.be'), allow_domains="openvld.be"),
            callback='parse_page', follow=True
        ),
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
