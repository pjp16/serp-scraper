import streamlit as st

st.write("hello")

import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession

with open('keywords.txt', 'r') as f:
    keywords = [line.strip() for line in f]

def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)
        
def scrape_google(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.com/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)

    return links[0:10]

output = {}

for k in keywords:
    urls = scrape_google(k)
    output[k] = urls

df = pd.DataFrame.from_dict(output, orient='index')
