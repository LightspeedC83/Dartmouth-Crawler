import requests
from bs4 import BeautifulSoup
import re 
from rich.console import Console 
from rich.progress import Progress

from .course import *

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



def construct_url(link, seed_domain, internal_marker):
    """takes a link and returns a valid link in the seed domain, run internal links through here to get consistent searchable links. 
    does nothing to non partial links."""
    # checking if url needs to be fixed becuase it's internal to the domain
    if link.startswith(internal_marker): # this means the link is internal
        link = f"{seed_domain}{link}"

    return link
   
    


def crawl(seed_urls,seed_domain, internal_marker, object_storage):
    """This function crawls all the links starting from a list of seed urls, staying within the seed domain. 
    The internal marker is what a link would start with if it is a subdomain link. 
    This function calls parse course on each url and adds the course object to the given object_storage set"""
    visited_links = {} # each link entry gets marked as visited here True = Visited
    queue = []
    for url in seed_urls:
        visited_links[url] = False
        queue.append(url)

    with Progress() as progress:    # setting up the progress indicator bar
        crawl_task = progress.add_task("[bold dark_green]Crawling... 0 Courses Found, 0 Sites Visited", total=len(queue))
              

        sites_visited = 0
        num_courses_found = 0
        while len(queue)>0:
            url = queue.pop(0)
            progress.update(crawl_task, total=len(queue))
            
            if url in visited_links and visited_links[url]: # if we've visited this link before
                continue

            # checking if url needs to be fixed becuase it's internal to the domain
            url = construct_url(url, seed_domain, internal_marker)

            # doing a bounds check to make sure the crawler doesn't go outside of the bounds defined by the seed urls
            if True not in [url.startswith(x) for x in seed_urls]:
                continue

            # if we make it this far, we will load the html from the page, we take note of that
            sites_visited+=1
            progress.update(crawl_task, advance=1, description=f"[bold dark_green]crawling... {num_courses_found} Courses Found. {sites_visited} Sites Visited. {len(queue)} Sites Left in Queue.  ")
            
            html = fetch_page(url) # getting the html from the page
            
            # mark link visited
            visited_links[url] = True
            if html is None:
                continue

            
            courseObject = parse_course(html,url)
            if courseObject is not None: # if page is a course page
                print("\u2713",url) # showing url, is a course
                object_storage.add(courseObject)
                num_courses_found+=1
                
            else:
                print("\u2718",url) # showing url, but not a course -- i don't want to hear the ai allegations on this unicode character insert! I searched those up to make it easier to read fast in the terminal thank you very much

            # getting all the links on this page and adding them to the queue
            links_on_this_page = parse_internal_links(html, internal_marker)
            for link in links_on_this_page:
                link = construct_url(link, seed_domain, internal_marker)
                if link in visited_links and visited_links[link]: continue # if we've visited this link before skip
                    
                queue.append(link)
        progress.update(crawl_task, completed=True)

    print("\nWebcrawl finished!")
        




def parse_course(html,url):
    """returns a Course object if the page is a dartmouth course page, otherwise None"""

    soup = BeautifulSoup(html, "html.parser")

    # im spacing it out in this way so we can expand the function later to already have everything needed to start building ✨objects✨ -- realize that if I put an emoji in this comment it makes it look like AI but i went and found that emoji FOR THE BIT. I refute the allegations
    degree_attributes = soup.find_all("div", class_="sc-extrafield")
    prereqs = soup.find_all("div", class_="sc_prereqs")
    coreqs = soup.find_all("div", class_="sc_coreqs")
    timetable = soup.find_all("div", class_="sc-timetable") # this seems to be all the same for every course

    offered = soup.find_all("div", class_="offered")
    description = soup.find_all("div", class_="desc")
    instructor = soup.find_all("div", class_="instructor")

    is_course = True in [len(x)>0 for x in [degree_attributes, prereqs, coreqs, timetable]] # a page is a course if the page has any of these things...

    if is_course:  
        course = Course(page_url=url) #creating course object
        # updating all the html attributes from what we have parsed
        course.prereqs_html = [str(x) for x in prereqs]
        course.degree_attributes_html = [str(x) for x in degree_attributes]
        course.coreqs_html = [str(x) for x in coreqs]
        course.offerings_html = [str(x) for x in offered]
        course.description_html = [str(x) for x in description]
        course.instructor_html = [str(x) for x in instructor]
        
        # getting the cross listed courses
        h2 = soup.find("h2", string=re.compile("Cross Listed Courses"))
        if h2 is not None:
            cross_lists = []
            for node in  h2.next_siblings:
                if node is None:  
                    continue
                if getattr(node, "name", None) == "div": # we've gotten to the end of the list (this is just seeing if the next sibling is a div)
                    break
                cross_lists.append(node)
            course.cross_lists_html = [str(x) for x in cross_lists]
            
        # getting department specific course categories
        h3 = soup.find("h3", string=re.compile("Department-Specific Course Categories"))
        if h3 is not None:
            categories = []
            for node in h3.next_siblings:
                if node is None:
                    continue
                if getattr(node, "name", None) == "div":
                    break
                categories.append(node.strip())
            course.department_category_html = [str(x) for x in categories]

        return course
        
            
    return None

    



    


def is_link_internal(url, internal_list):
    """returns true if the link is internal to where we want to keep the search 
    (ie. returns true if the given url is a subdomain of any link in the internal list)"""

    for valid in internal_list:
        if url.startswith(valid): return True

    return False