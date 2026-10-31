import requests
from bs4 import BeautifulSoup
from typing import List, Tuple

# we will use a user agent header to make our request to the website look like a normal user and not a bot
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

def fetch_page(url):
    """downloads a page and returns the html content (type <class 'bytes'>). raises an error on bad lookup"""
    response = requests.get(url) # http response object using requests library
    response.raise_for_status() # this will raise an error if we get a bad lookup
    
    return response.content

def parse_internal_links(html):
    """"""
    soup = BeautifulSoup(html, "html.parser")

    return [ x["href"] for x in soup.find_all("a") if x["href"].startswith("/en")]

    # results = soup.find(id="rightpanel")
    # print(results.prettify())

    # for x in soup.find_all("a"):
    #     href = x["href"]

    #     if href.startswith("/en"):
    #         return href