# Dartmouth Webcrawler
I was bored and doing my university course selection. It got me wondering what the most needed prerequisite was, and what class needed the most prerequisites, and so on, and so forth...

I am also using this as an opportunity to learn how to effectively use uv to manage my python projects

# Notes about the dartmouth course catalog 
- The seed urls we are starting with have a lot of links to different departments, which in turn have links to a page that lists all of that department's courses (amongst many other links)
- The two seed urls are the roots of the link tree that we want to stay inside of
- a class page will have a `<div class="sc-extrafield">` with an `<h3>` with the text "Degree Requirement Attributes". This should always be there from what I can tell. However, even if the course has no prereqs or coreqs, the page will have empty `<div class="sc_prereqs">` and `<div class="sc_coreqs">`. Also a page should alwyas have a `<div class="sc-timetable">`.
- A course title can be found in a course page from:
    the 4 letter code followed by a number held in a `<span>` within an `<h1>` within a `<div id="main">` 
        ```html
        <div id="main">
            <h1>
                <span>COSC 1</span> Introduction to Programming and Computation
            </h1>
            ...
        </div>
        ```
- the department a course is associated with can be gotten from the page link like so: `{seedurl}/{department_name}/...`

# Sources
- [this](https://www.scrapingbee.com/blog/crawling-python/) blog post by Ari Bajo was very helpful to learn about webcrawling.
- [this blog](https://realpython.com/beautiful-soup-web-scraper-python/#explore-the-website) by Martin Breuss on realpython was also super helpful and descriptive.

# Todo:
- crawl the dartmouth catalog
- Get the data from the dartmouth catalog
- get the course information from the page data and represent it in a graph
- visualize the graph

# other ideas
- adapt this to webscrape for job/internship openings then collect it in one place
    - hook this up to an llm to find ones that fit you and and then 


