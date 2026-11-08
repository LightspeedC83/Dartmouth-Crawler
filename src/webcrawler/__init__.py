
from .crawler import *
from .course import *
from .data_storage import *



def main() -> None:
    
    clean_course_html(load_filepath="./src/data/crawler_data_full_sweep_11.7.26.pkl", save_filepath="./src/data/processed_data_full_sweep.pkl")

    # clean_course_html(load_filepath="./src/data/crawler_data.pkl", save_filepath="./src/data/processed_data_full_sweep.pkl")

    # crawl_dartmouth_courses("./src/data/crawler_data.pkl")


def crawl_dartmouth_courses(save_filepath):
    """crawls the dartmouth course catalog"""

    seed_urls = ["https://dartmouth.smartcatalogiq.com/en/current/orc/departments-programs-undergraduate/engineering-sciences/engs-engineering-sciences-undergraduate",
             "https://dartmouth.smartcatalogiq.com/en/current/orc/departments-programs-undergraduate/", 
             "https://dartmouth.smartcatalogiq.com/en/current/orc/departments-programs-graduate",
             "https://dartmouth.smartcatalogiq.com/en/2026s/supplement/new-undergraduate-courses"]
    seed_domain = "https://dartmouth.smartcatalogiq.com"
    internal_marker = "/en"

    print("initiating webcrawl...\n")

    courses = set() # set with all the course objects in it

    try:        
        crawl(seed_urls, seed_domain, internal_marker, object_storage=courses)

    except KeyboardInterrupt:
        print("user has interrupted the search")
    except Exception as e:
        print(f"the search has been interrupted: {e}")

    # either it goes until it's done or the user stops the search, at the end we store the result
    save_data(save_filepath, courses, overwrite=True)


def clean_course_html(load_filepath, save_filepath):
    """loads in dartmouth courses from a pickled file, cleans the html"""
    
    print(f"loading {load_filepath}")
    
    try:
        course_set = load_data(load_filepath) # load in from pickle
    except FileNotFoundError as e:
        print(f"File was Not able to be located: \n{e}")

    # call object methods to clean the html
    for course in course_set:
        # course.process_all_data()
        course.process_department_category()

    save_data(save_filepath, course_set, overwrite=True)
    