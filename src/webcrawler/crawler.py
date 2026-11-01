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
    try:

        response = requests.get(url) # http response object using requests library
        response.raise_for_status() # this will raise an error if we get a bad lookup
        return response.content
    except requests.exceptions.HTTPError or requests.exceptions.RequestException:
        return None


def parse_internal_links(html, internal_link_starts_with):
    """when given html content, this function uses beautiful soup to find all the links that are internal."""
    soup = BeautifulSoup(html, "html.parser")

    return [ x["href"] for x in soup.find_all("a", href=True) if x["href"].startswith(internal_link_starts_with)]

    # results = soup.find(id="rightpanel")
    # print(results.prettify())

    # for x in soup.find_all("a"):
    #     href = x["href"]

    #     if href.startswith("/en"):
    #         print(href)






def parse_course(html):
    """returns true if the page is a dartmouth course page"""

    soup = BeautifulSoup(html, "html.parser")

    # im spacing it out in this way so we can expand the function later to already have everything needed to start building ✨objects✨ -- realize that if I put an emoji in this comment it makes it look like AI but i went and found that emoji FOR THE BIT. I refute the allegations
    degree_attributes = soup.find_all("div", class_="sc-extrafield")
    prereqs = soup.find_all("div", class_="sc_prereqs")
    coreqs = soup.find_all("div", class_="sc_coreqs")
    timetable = soup.find_all("div", class_="sc-timetable")
   
    return True in [len(x)>0 for x in [degree_attributes, prereqs, coreqs, timetable]] # returns true if the page has any of these things
    



    


def is_link_internal(url, internal_list):
    """returns true if the link is internal to where we want to keep the search 
    (ie. returns true if the given url is a subdomain of any link in the internal list)"""

    for valid in internal_list:
        if url.startswith(valid): return True

    return False