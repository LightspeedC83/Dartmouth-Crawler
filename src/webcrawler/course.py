from bs4 import BeautifulSoup

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
        # not having a processed description, we can just render the html if we want to visualize it
        self.instructor = None
        self.department_category = None # will be a string


    def process_all_data(self):
        """this method processes all the html data into useful object properties"""

        self.process_prereqs_data()
        self.process_degree_attributes_data()
        self.process_cross_lists_data()
        # self.process_coreqs_data()
        self.process_offerings_data()
        self.process_instructor()
        self.process_department_category()

        
    def process_prereqs_data(self):
        """This method parses the prereqs_htm class parameter and uses its data to update the prereqs parameter, which should be directly accessible\n
        The prereqs data is usually in a buch of `<a>` tags it seems. oftentimes, they have a href link on the rereq """
        if self.prereqs_html is None or len(self.prereqs_html) == 0:
                return False

        # TODO: custom body to process the html

        pass

    
    def process_degree_attributes_data(self):
        """This method parses the degree_attr class parameter and uses its data to update the degree_attributes parameter, which should be directly accessible"""
        if self.degree_attributes_html is None or len(self.degree_attributes_html) == 0:
                return False

        # TODO: custom body to process the html

        pass

    
    def process_cross_lists_data(self):
        """This method parses the cross_lists class parameter and uses its data to update the cross_lists parameter, which should be directly accessible"""
        if self.cross_lists_html is None or len(self.cross_lists_html) == 0:
            return False
        
        # TODO: Some cross lists that are multiple classes in one string need to be separated (eg. "ARAB 61.10 COLT 62.10 MES 16.08")
        output_list = [x.strip(",").strip(";").strip() for x in self.cross_lists_html if x.strip() not in [",",";",""]]
        self.cross_lists = []
        for item in output_list:
            soup = BeautifulSoup(item, "html.parser")
            to_add = item   

            if soup.find("a", href=True): # if our element is acutally a link to another course, we replace it with the string text name for said course
                x=soup.find_all("a", href=True)[0].text
                to_add = x

            split = to_add.strip().split(" ")
            if len(split) > 2: # a normal class would have [character sequence] [space] [number sequence], which results in a lenght of two when split by space
                list_to_add = []
                prev_component = None
                for component in to_add.strip().split(" "):
                    if prev_component != None:
                        course_name = prev_component + " " + component
                        list_to_add.append(course_name.strip().strip(";").strip(","))
                        prev_component = None
                    else:
                        prev_component = component

                self.cross_lists += list_to_add # add each new class name item to the cross list list

            else:
                self.cross_lists.append(to_add.strip().strip(";").strip(","))  
            

        return True

        
    # def process_coreqs_data(self):
    #     """This method parses the coreqs_html class parameter and uses its data to update the coreqs parameter, which should be directly accessible"""
    #     if self.coreqs_html is None or len(self.coreqs_html) == 0:
    #         return False

    #     # There are no coreqs data, seems like it's not a thing. They're all empty (if they're all empty why is there a section for them on the registrar sites??)
    #     pass

    
    def process_offerings_data(self):    
        """This method parses the offerings_html class parameter and uses its data to update the offerings parameter, which should be directly accessible"""
        if self.offerings_html is None or len(self.offerings_html) == 0:
            return False

        # currently all offerings lists are 1 element long (or empty)
        self.offerings = []

        soup = BeautifulSoup(self.offerings_html[0], "html.parser")
        terms_html = soup.find_all("li")
        for x in terms_html:
            self.offerings.append(x.text)

        return True


    def process_instructor(self):
        """This method parses the instructor_html class parameter and uses its data to update the coreqs parameter, which should be directly accessible"""
        if self.instructor_html is None or len(self.instructor_html) == 0:
            return False

        # TODO: make sure we're not misssing anything
        soup = BeautifulSoup(self.instructor_html[0], "html.parser")
        instructor = soup.find("div", id="instructor").text[10:]

        print(instructor)

        pass


    def process_department_category(self):
        """This method parses the department_category_html class parameter and uses its data to update the coreqs parameter, which should be directly accessible"""
        if self.department_category_html is None or len(self.department_category_html) == 0:
            return False

        # the list we get loaded in with will always be length 1, we now need to split this up...
        # ...the thing is that, it's always one thing and if it splits up, it does so based on class year.
        # meaning if we split, we can separate by class year, but it might look like there are multiple department course categories,
        # but actually it's one department course category that changed over time. I'll include code to split up here, but commented out
        # 
        # but there can be multiple department course categories, which are separated by a comma after the word class of XXXX and beyond/before, which usually has a ";" separator (i found one case where it had this sturcture but no ";" separator: 'Class of 2024 and Beyond Major/Minor Dist: US, modern.').
        #  commas appear elsewhere, but it seems if they do they're part of a sentence and have no significance. 
        # 
        # output_list =self.department_category_html 
        # if ";" in  output_list[0]:
        #     output_list = output_list[0].split(";")      
        # self.department_category = output_list

        self.department_category = self.department_category_html[0]
        # print(self.department_category)
        return True
        
        

        

