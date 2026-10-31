seed_urls = ["https://dartmouth.smartcatalogiq.com/en/current/orc/departments-programs-undergraduate/"]
seed_domains = ["https://dartmouth.smartcatalogiq.com"]

from .crawler import *

def main() -> None:
    print("initiating webcrawl...\n")
    html = fetch_page(seed_urls[0])

    for x in parse_internal_links(html):
        print(x)