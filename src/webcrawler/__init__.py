seed_urls = ["https://dartmouth.smartcatalogiq.com/en/current/orc/departments-programs-undergraduate/", "https://dartmouth.smartcatalogiq.com/en/current/orc/departments-programs-graduate"]
seed_domain = "https://dartmouth.smartcatalogiq.com"
internal_marker = "/en"

from .crawler import *

def main() -> None:
    print("initiating webcrawl...\n")

    visited_links = {} # each link entry gets marked as visited here True = Visited
    queue = []
    for url in seed_urls:
        visited_links[url] = False
        queue.append(url)

    while len(queue)>0:
        url = queue.pop()
        print(url)
        if url in visited_links and visited_links[url]: # if we've visited this link before
            continue

        if url.startswith(internal_marker): # this means the link is internal
            html = fetch_internal_page(url, seed_domain)
            
        elif url.startswith(seed_domain):
            html = fetch_page(url) # getting the html from the page

        # mark link visited
        visited_links[url] = True
        if html is None:
            continue
        
        links_on_this_page = parse_internal_links(html, internal_marker)
        for link in links_on_this_page:
            queue.append(link)
        


   
    
