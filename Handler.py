import os
import requests
import re
import csv
import threading
import cProfile
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from course import Course
from queue import Queue
import time

# URL of the Chapman course catalog
URL = "https://catalog.chapman.edu/content.php?catoid=46&navoid=2420"
parentPage = requests.get(URL)  # Sends a request to fetch the webpage content

# Creates a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(parentPage.content, "html.parser")

# Thread lock for thread-safe file writing
file_lock = threading.Lock()

def get_prerequisites(catoid, coid, retries=3):
    """Fetches prerequisites using an AJAX request with retries."""
    ajax_url = f"https://catalog.chapman.edu/ajax/preview_course.php?catoid={catoid}&coid={coid}&show"
    for attempt in range(retries):
        try:
            time.sleep(1.1)  # Add a delay between retries
            response = requests.get(ajax_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                prereq_div = soup.find("div", class_=None)
                if prereq_div:
                    return prerequisite_allocator(prereq_div.text.strip())
            raise Exception("Error loading source page")
        except Exception as e:
            if attempt == retries - 1:  # If this is the last attempt, raise the exception
                raise e
            print(f"Attempt {attempt + 1} failed. Retrying...")

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

def parse_course_info(course_element, category):
    """Extracts course name, credits, and prerequisites from the course element."""
    course_text = course_element.text.strip()
    match = re.search(r'(.+?)\s+([\d½¾¼.]+-[\d½¾¼.]+|[\d½¾¼.]+)\s+credits', course_text)
    if match:
        obj_name = match.group(1).strip()
        obj_credits = match.group(2)
        
        # Extract catoid and coid from onclick event
        onclick_attr = course_element.find("a")["onclick"] if course_element.find("a") else ""
        catoid_match = re.search(r"showCourse\('\d+', '(\d+)',", onclick_attr)
        coid_match = re.search(r"showCourse\('(\d+)',", onclick_attr)
        catoid = coid_match.group(1) if coid_match else ""
        coid = catoid_match.group(1) if catoid_match else ""
        
        prerequisites = get_prerequisites(catoid, coid) if catoid and coid else "No prerequisites found"
        return Course(obj_name, obj_credits, prerequisites, category)
    else:
        print(course_element.prettify())
        print("Course format not accepted")

def parse_courses(soupObj):
    """Extracts course details from a degree page and returns a list of Course objects."""
    courseList = []
    catalog_group = soupObj.find("div", class_="custom_leftpad_20")
    if catalog_group:
        course_categories = catalog_group.find_all("div", class_="acalog-core")
        if course_categories:
            for categories in course_categories:
                category = categories.find("h2").text.strip().split('(')[0].strip()
                course_elements = categories.find_all("li", class_="acalog-course")
                
                # Use a thread-safe queue to collect results
                result_queue = Queue()
                
                def process_course(course, category):
                    """Process a single course and put the result in the queue."""
                    if "credits" in course.text.strip():
                        try:
                            tempCourse = parse_course_info(course, category)
                            if tempCourse:
                                result_queue.put(tempCourse)
                        except Exception as e:
                            print(f"Error processing course: {e}")
                
                # Use ThreadPoolExecutor to process each course in parallel
                with ThreadPoolExecutor(max_workers=5) as executor:  # Limit to 5 threads
                    futures = [executor.submit(process_course, course, category) for course in course_elements]
                    
                    # Wait for all threads to complete
                    for future in futures:
                        future.result()
                
                # Transfer results from the queue to the courseList
                while not result_queue.empty():
                    courseList.append(result_queue.get())
        
    return courseList

def process_degree(degree, folder_name):
    """Processes a single degree and writes its courses to a CSV file."""
    degree_name = degree.text.strip()
    if " B." in degree_name:  # Skip minors (all bachelors degrees contain suffix with 'B.')
        degree_ref = degree["href"]
        complete_url = f"https://catalog.chapman.edu/{degree_ref}"
        degree_response = requests.get(complete_url)
        coursesoup = BeautifulSoup(degree_response.content, "html.parser", from_encoding="utf8")
        valid_filename = "".join(c for c in degree_name if c.isalnum() or c in (' ', '_')).rstrip()
        file_path_csv = os.path.join(folder_name, f"{valid_filename}.csv")
        
        # Write course data
        courses = parse_courses(coursesoup)
        rows = [["Course Name", "Credits", "Prerequisites", "Category"]]  # Header row
        for course in courses:
            # Format prerequisites as a comma-separated string
            prereqs = ", ".join(course.prerequisites) if isinstance(course.prerequisites, list) else course.prerequisites
            rows.append([course.name, course.credits, prereqs, course.category])

        # Write to CSV
        with file_lock:  # Ensure thread-safe file writing
            with open(file_path_csv, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)  # Write all rows at once
                
        print(f'Saved: {file_path_csv}')

def parse_college():
    """Extracts degree program links and processes each degree to fetch its courses."""
    folder_name = 'Output'  # Folder to store the parsed course data
    cwd = os.getcwd()
    final_dr = os.path.join(cwd, folder_name)
    print(final_dr)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    degree_header = soup.find("h4", string="Degrees")  # Locate the 'Degrees' section
    if degree_header:
        # Finds all siblings below the degree text on the page which contain a 'program list'
        program_list = degree_header.find_next_siblings("ul", class_="program-list")
        if program_list:
            # Collect all degree links
            degrees = []
            for subcategory in program_list:
                degrees.extend(subcategory.find_all("a"))
            
            # Create a queue for degrees
            degree_queue = Queue()
            for degree in degrees:
                degree_queue.put(degree)
            
            # Define a worker function to process degrees from the queue
            def degree_worker():
                while not degree_queue.empty():
                    try:
                        degree = degree_queue.get()
                        process_degree(degree, folder_name)
                    except Exception as e:
                        print(f"Error processing degree: {e}")
                    finally:
                        degree_queue.task_done()
            
            # Use ThreadPoolExecutor to process degrees concurrently
            with ThreadPoolExecutor(len(degrees)) as executor:
                futures = [executor.submit(degree_worker) for _ in range(5)]
                
                # Wait for all threads to complete
                for future in futures:
                    future.result()
        else:
            print("No program list found.")
    else:
        print("No 'Degrees' header found.")

def main(): 
        cProfile.run('parse_college()')

main()