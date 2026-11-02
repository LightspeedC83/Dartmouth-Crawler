

class Course(): 

    def __init__(self, page_url=""):

        self.page_url = page_url

        # the html from the website that we get for the courses
        self.prereqs_html = None 
        self.degree_attributes_html = None 
        self.cross_lists_html = None # these are the only two without a div
        self.coreqs_html = None
        self.offerings_html = None
        self.description_html = None
        self.instructor_html = None
        self.department_category_html = None # these are the only two without a div

        # these will be the informations once extracted from each _html parameter
        self.prereqs = None
        self.degree_attributes = None
        self.cross_lists = None
        self.coreqs = None
        self.offerings = None

    
    def process_prereqs_data(self):
        """This method parses the prereqs_htm class parameter and uses its data to update the prereqs parameter, which should be directly accessible\n
        The prereqs data is usually in a buch of `<a>` tags it seems. oftentimes, they have a href link on the rereq """
        if len(self.prereqs_html) == 0: return False
        # TODO: custom body to process the html

        pass

    
    def process_degree_attributes_data(self):
        """This method parses the degree_attr class parameter and uses its data to update the degree_attributes parameter, which should be directly accessible"""
        if len(self.degree_attributes_html) == 0: return False
        # TODO: custom body to process the html

        pass

    
    def process_cross_lists_data(self):
        """This method parses the cross_lists class parameter and uses its data to update the cross_lists parameter, which should be directly accessible"""
        if len(self.cross_lists_html) == 0: return False
        # TODO: custom body to process the html

        pass

    
    def process_coreqs_data(self):
        """This method parses the coreqs_html class parameter and uses its data to update the coreqs parameter, which should be directly accessible"""
        if len(self.coreqs_html) == 0: return False
        # TODO: custom body to process the html

        pass

    
    def process_offerings_data(self):    
        """This method parses the offerings_h class parameter and uses its data to update the offerings parameter, which should be directly accessible"""
        if len(self.offerings_html) == 0: return False
        # TODO: custom body to process the html

        pass
