import os
import requests
import re
from bs4 import BeautifulSoup
from course import Course

# URL of the Chapman course catalog
URL = "https://catalog.chapman.edu/content.php?catoid=46&navoid=2420"
parentPage = requests.get(URL)  # Sends a request to fetch the webpage content

# Creates a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(parentPage.content, "html.parser")

def get_prerequisites(catoid, coid):
    """Fetches prerequisites using an AJAX request."""
    ajax_url = f"https://catalog.chapman.edu/ajax/preview_course.php?catoid={catoid}&coid={coid}&show"
    response = requests.get(ajax_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        prereq_div = soup.find("div", class_=None)
        if prereq_div:
            return prerequisite_allocator(prereq_div.text.strip())
    raise Exception("Error loading source page")

def prerequisite_allocator(text: str):
    if text:    
        # Find the starting point of "Prerequisites" or "Prerequisite"
        prerequisite_keyword = None
        if "Prerequisites, " in text:
            prerequisite_keyword = "Prerequisites, "
        elif "Prerequisite, " in text:
            prerequisite_keyword = "Prerequisite, "
        else:
            return "N/A"

        if prerequisite_keyword:
            # Find the index where the keyword starts
            start_index = text.find(prerequisite_keyword) + len(prerequisite_keyword)
            # Extract the substring starting after the keyword
            text = text[start_index:]

        
        prerequisites = []

        text = text.replace("\xa0", " ") # Replaces instances of HTML Non-breaking space with a normal space character
        text = text.replace(" or", ",") # Replaces instances of 'or ' with a ',' to split up phrases and solve redundancy in phrases
        text = text.replace(",,", ",") # fixes last lines issues
        # Split the string at commas and stop at the first period
        for phrase in text.split(","):
            phrase = phrase.strip()  # Remove leading/trailing whitespace
            if "." in phrase:  # Stop at the first period
                phrase = phrase.split(".")[0]  # Take only the part before the period
                prerequisites.append(phrase)
                break  # Exit the loop after the first period
            prerequisites.append(phrase)
        return prerequisites
    else:
        raise Exception("No text found in AJAX request.")

def parse_course_info(course_element):
    """Extracts course name, credits, and prerequisites from the course element."""
    course_text = course_element.text.strip()
    match = re.search(r'(.+?)\s+(\d+)\s+credits', course_text)
    if match:
        obj_name = match.group(1).strip()
        obj_credits = int(match.group(2))
        
        # Extract catoid and coid from onclick event
        onclick_attr = course_element.find("a")["onclick"] if course_element.find("a") else ""
        catoid_match = re.search(r"showCourse\('\d+', '(\d+)',", onclick_attr)
        coid_match = re.search(r"showCourse\('(\d+)',", onclick_attr)
        catoid = coid_match.group(1) if coid_match else ""
        coid = catoid_match.group(1) if catoid_match else ""
        
        prerequisites = get_prerequisites(catoid, coid) if catoid and coid else "No prerequisites found"
        return Course(obj_name, obj_credits, prerequisites)
    else:
        print("Course format not accepted")

def parse_courses(soupObj):
    """Extracts course details from a degree page and returns a list of Course objects."""
    courseList = []
    catalog_group = soupObj.find("div", class_="custom_leftpad_20")
    if catalog_group:
        course_elements = catalog_group.find_all("li", class_="acalog-course")
        for course in course_elements:
            if "credits" in course.text.strip():
                tempCourse = parse_course_info(course)
                courseList.append(tempCourse)
    return courseList

def parse_college():
    """Extracts degree program links and processes each degree to fetch its courses."""
    folder_name = 'Dodge'  # Folder to store the parsed course data
    cwd = os.getcwd()
    final_dr = os.path.join(cwd, folder_name)
    print(final_dr)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    degree_header = soup.find("h4", string="Programs")  # Locate the 'Programs' section
    if degree_header:
        program_list = degree_header.find_next_sibling("ul", class_="program-list")
        if program_list:
            degrees = program_list.find_all("a")  # Find all program links
            for degree in degrees:
                degree_name = degree.text.strip()
                degree_ref = degree["href"]
                complete_url = f"https://catalog.chapman.edu/{degree_ref}"
                degree_response = requests.get(complete_url)
                coursesoup = BeautifulSoup(degree_response.content, "html.parser")
                valid_filename = "".join(c for c in degree_name if c.isalnum() or c in (' ', '_')).rstrip()
                file_path_txt = os.path.join(folder_name, f"{valid_filename}.txt")
                print(file_path_txt)
                with open(file_path_txt, "w", encoding="utf-8") as f:
                    courses = parse_courses(coursesoup)
                    for course in courses:
                        f.write(f"{course.name} ({course.credits} credits)\nPrerequisites: {course.prerequisites}\n\n")
                print(f'Saved: {file_path_txt}')
        else:
            print("No program list found.")
    else:
        print("No 'Degrees' header found.")

def main():
    """Main function to initiate the parsing process based on user input."""
    run_parse_header = input("Would you like to create the main html parser? y or n: \n")
    if run_parse_header == "y":
        parse_college()

main()
