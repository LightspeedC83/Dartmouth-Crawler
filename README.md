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
- [this](https://www.scrapingbee.com/blog/crawling-python/) blog post by Ari Bajo was helpful to learn about webcrawling.
- [this blog](https://realpython.com/beautiful-soup-web-scraper-python/#explore-the-website) by Martin Breuss on realpython was also super helpful and descriptive, especially for using beautiful soup for webscraping.

# Todo:
- ~~crawl the dartmouth catalog~~
- ~~Get the data from the dartmouth catalog~~
- ~~determine whether or not a page is for a course~~
- ~~get a bunch of examples by manually combing the catalog~~
- ~~get the course information html from the page & create object structure~~
	- fix issue with instructor data not making it into the course object
- extract data from the html 
- represent data in a graph (networkx)
- visualize the graph

# other ideas
- adapt this to webscrape for job/internship openings then collect it in one place
    - hook this up to an llm to find ones that fit you and and then 


# Things I learned on this project
- how to use uv
- webcrawling and webscraping with requests and beatifulsoup
- using rich to make the terminal look better
- pickling 


# Notes:
- for prereq description:
	- some courses will be listed as [department code] [one number]/[other number] -- we need to parse at least one of these numbers
	- 

# HTML examples
The first thing I did was look through the site I wanted to scrape. I used inspect element to get a bunch of examples of the html for different parts of the page I was interested in.  I've collected those examples below:

## sc_prereqs
```html
<div class="sc_prereqs">
	<h2>
		Prerequisite
	</h2><a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/computer-science/cosc-computer-science-undergraduate/cosc-1">COSC 1</a>. Recommended Preparation: <a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/mathematics/math-mathematics-undergraduate/math-3">MATH 3</a>, <a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/mathematics/math-mathematics-undergraduate/math-8">MATH 8</a> or <a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/mathematics/math-mathematics-undergraduate/math-9">MATH 9</a>.
</div>

```

```html
<div class="sc_prereqs">

</div>
```

```html
<div class="sc_prereqs">
	<h2>
		Prerequisite
	</h2><a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/computer-science/cosc-computer-science-undergraduate/cosc-70">COSC 70</a>. Recommended Preparation: <a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/computer-science/cosc-computer-science-undergraduate/cosc-50">COSC 50</a>.
</div>
```

```html
<div class="sc_prereqs">
	<h2>
		Prerequisite
	</h2><a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/government/govt-government/introductory-courses/govt-4">GOVT 4</a> is strongly recommended but not required.
</div>
```

```html
<div class="sc_prereqs">
	<h2>
		Prerequisite
	</h2><a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/computer-science/cosc-computer-science-undergraduate/cosc-78">COSC 78</a>. Recommended Preparation: Experience with building, modifying and training a deep learning model.
</div>

```

```html
<div class="sc_prereqs">
	<h2>
		Prerequisite
	</h2><a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/computer-science/cosc-computer-science-undergraduate/cosc-78">COSC 78</a>. Recommended Preparation: Experience with building, modifying and training a deep learning model.
</div>

```

```html
<div class="sc_prereqs">
	<h2>
		Prerequisite
	</h2><a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/engineering-sciences/engs-engineering-sciences-undergraduate/engs-24">ENGS 24</a> and <a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/engineering-sciences/engs-engineering-sciences-undergraduate/engs-33">ENGS 33</a> or equivalent
</div>

```

```html
<div class="sc_prereqs">
	<h2>
		Prerequisite
	</h2>Permission of the department chair. (One-page proposal submission required and must be submitted for approval prior to the end of the term preceding the term in which the course will be taken.)
</div>
```

```html
<div class="sc_prereqs">
	<h2>
		Prerequisite
	</h2><a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/mathematics/math-mathematics-undergraduate/math-46">MATH 46</a> or <a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/engineering-sciences/engs-engineering-sciences-undergraduate/engs-22">ENGS 22</a> and <a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/engineering-sciences/engs-engineering-sciences-undergraduate/engs-23">ENGS 23</a> or the equivalent
</div>

```

```html
<div class="sc_prereqs">
	<h2>
		Prerequisite
	</h2><a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/engineering-sciences/engs-engineering-sciences-undergraduate/engs-21">ENGS 21</a> plus one of the following: <a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/engineering-sciences/engs-engineering-sciences-undergraduate/engs-31">ENGS 31</a>, <a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/engineering-sciences/engs-engineering-sciences-undergraduate/engs-32">ENGS 32</a>, <a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/engineering-sciences/engs-engineering-sciences-undergraduate/engs-33">ENGS 33</a>, <a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/engineering-sciences/engs-engineering-sciences-undergraduate/engs-35">ENGS 35</a>, <a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/engineering-sciences/engs-engineering-sciences-undergraduate/engs-36">ENGS 36</a>, <a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/engineering-sciences/engs-engineering-sciences-undergraduate/engs-37">ENGS 37</a>, or <a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/engineering-sciences/engs-engineering-sciences-undergraduate/engs-56">ENGS 56</a>. Experience with SolidWorks is helpful but not required.
</div>
```

```html
<div class="sc_prereqs">
<h2>
                Prerequisite
        </h2>Written permission of the department faculty member who will be advising the student.
</div>

```

```html
<div class="sc_prereqs">
<h2>
                Prerequisite
        </h2>(<a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/biological-sciences/biol-biological-sciences-undergraduate/biol-12">BIOL 12</a> or <a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/biological-sciences/biol-biological-sciences-undergraduate/biol-19">BIOL 19</a>) and (<a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/chemistry/chem-chemistry-undergraduate/chem-52">CHEM 52</a> or CHEM 58); or Instructor Permission.
</div>
```

```html
<div class="sc_prereqs">
<h2>
                Prerequisite
        </h2>Animation: Principles and Practice or previous animation experience. Permission of the instructor required.
</div>
```



## cross listing examples
```html
<h2>
	Cross Listed Courses
</h2>
"ENGL 53.54 WGSS 66.27"
```

```html
<h2>
	Cross Listed Courses
</h2>
"COCO 033 EEER 38.15 JWST 05.01"
```

```html
<h2>
	Cross Listed Courses
</h2>
"COSC 189"
```

```html
<h2>
	Cross Listed Courses
</h2>
<a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/physics-and-astronomy/phys-physics-undergraduate/phys-70">PHYS 70</a>

```

```html
<h2>
	Cross Listed Courses
</h2>
<a class="sc-courselink" href="/en/current/orc/departments-programs-undergraduate/computer-science/cosc-computer-science-undergraduate/cosc-65">COSC 65</a>, <a class="sc-courselink" href="/en/current/orc/departments-programs-graduate/computer-science/cosc-computer-science/100/cosc-165">COSC 165</a>
```
it seems like always after cross listed courses comes sc_prereqs


## Degree requirement attributes examples
```html
<div class="sc-extrafield">
	<h3>
		Degree Requirement Attributes
	</h3><p>Dist:INT or SOC</p>
</div>
```
```html
<div class="sc-extrafield">
	<h3>
		Degree Requirement Attributes
	</h3><p>Dist:INT or SOC; WCult:CI</p>
</div>
```

## department specific course categories
```html
<h3>
	Department-Specific Course Categories
</h3>
"Classics  - Classical Studies Greek Latin"
                                        
```

## instructor
```html
<div id="instructor"><h3>Instructor</h3>Carpenter-Song</div>
```
```html
<div id="instructor"><h3>Instructor</h3>Kan</div>
```

## offerings
```html
<div class="offered">
	<h2>
		Offered
	</h2><ul>
		<li>Spring</li><li>Winter</li>
	</ul>
</div>


```