seed_urls = ["https://dartmouth.smartcatalogiq.com/en/current/orc/departments-programs-undergraduate/", "https://dartmouth.smartcatalogiq.com/en/current/orc/departments-programs-graduate", "https://dartmouth.smartcatalogiq.com/en/2026s/supplement/new-undergraduate-courses"]
seed_domain = "https://dartmouth.smartcatalogiq.com"
internal_marker = "/en"

from .crawler import *
from .course import *

courses = set() # set with all the course objects in it

def main() -> None:
    print("initiating webcrawl...\n")

    visited_links = {} # each link entry gets marked as visited here True = Visited
    queue = []
    for url in seed_urls:
        visited_links[url] = False
        queue.append(url)

    while len(queue)>0:
        url = queue.pop(0)
        
        
        if url in visited_links and visited_links[url]: # if we've visited this link before
            continue

        # checking if url needs to be fixed becuase it's internal to the domain
        url = construct_url(url)

        # doing a bounds check to make sure the crawler doesn't go outside of the bounds defined by the seed urls
        if True not in [url.startswith(x) for x in seed_urls]:
            continue

        
        html = fetch_page(url) # getting the html from the page

        # mark link visited
        visited_links[url] = True
        if html is None:
            continue

        
        courseObject = parse_course(html,url)
        if courseObject is not None:
            print("\u2713",url) # showing url, is a course
            courses.add(courseObject)
        else:
            print("\u2718",url) # showing url, but not a course -- i don't want to hear the ai allegations on this unicode character insert! I searched those up to make it easier to read fast in the terminal thank you very much

        # getting all the links on this page and adding them to the queue
        links_on_this_page = parse_internal_links(html, internal_marker)
        for link in links_on_this_page:
            link = construct_url(link)
            if link in visited_links and visited_links[link]: continue # if we've visited this link before skip
                
            queue.append(link)
        


def construct_url(link):
    """takes a link and returns a valid link in the seed domain, run internal links through here to get consistent searchable links. 
    does nothing to non partial links."""
    # checking if url needs to be fixed becuase it's internal to the domain
    if link.startswith(internal_marker): # this means the link is internal
        link = f"{seed_domain}{link}"

    return link
   
    
