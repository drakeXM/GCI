# Chapman directory webscraper

# Import necessary packages
import os
import requests
from bs4 import BeautifulSoup

# Creates a request object
URL = "https://catalog.chapman.edu/content.php?catoid=46&navoid=2429"
parentPage = requests.get(URL)

# Creates a soup object which scrapes the page content from the request object
soup = BeautifulSoup(parentPage.content, "html.parser")

def create_troubleshoot():
    
    # Creates a more legible string to be sent to a text file
    text = soup.prettify()

    # Creates a file which contains the prettified HTML
    with open("raw.html", "w", encoding="utf-8") as f:
        f.write(text)

    with open("links.html", "w", encoding="utf-8") as f:
        for link in soup.find_all('a'):
            linkString = link.get('href')
            f.write(f"{linkString}\n")
    print("Files created successfully")

# Returns courses offered per degree
def parse_courses(soupObj):
    
    final_text = ""

    # searches for all 'div' with the class 'program_description'
    catalog_group = soupObj.find("div", class_="custom_leftpad_20")

    if catalog_group:

        # Fetches all 'h2' tags within 'div'
        group_name_tags = catalog_group.find_all("h2")
        
        for name in group_name_tags:
            
            # Returns name of course category and adds it to final_text
            group_name = name.text.strip()
            final_text += f"\n{group_name}\n\n"

            course_element = name.find_next_sibling("ul")
            
            
            if course_element:

                # course_element_text = course_element.prettify()
                # final_text += f"{course_element_text}"

                contained_courses = course_element.find_all("li")

                for course in contained_courses:

                    for course_name in course.find_all("a"):
                        
                        if course_name.text.strip() != "":

                            final_text += f"\t--{course.text.strip()}\n\n"


            else:
                print("No course element found")
    else:
        print("no catalog group found")
    
    return final_text

def parse_college():
    
    # Create the "Fowler" folder if it doesn't exist
    folder_name = 'Fowler'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Verify that the HTML file contains a header with the text 'Degrees'
    degree_header = soup.find("h4", text="Degrees")



    if degree_header:

        # Grabs the information in the sibling tag <ul>
        program_list = degree_header.find_next_sibling("ul", class_="program-list")

        if program_list:
            
            # Finds all links under <a> tag
            degrees = program_list.find_all("a")

            for degree in degrees:

                # parses through all degrees and retrieves the name and reference link of the catalog
                degree_name = degree.text.strip()
                degree_ref = degree["href"]

                # Creates a url legible to requests
                complete_url = f"https://catalog.chapman.edu/{degree_ref}"

                # Fetch the HTML content from the degree URL
                degree_response = requests.get(complete_url)

                # creates another soup object which continuously reads each new webpage
                coursesoup = BeautifulSoup(degree_response.content, "html.parser")

                # Clean the degree name to make it a valid filename
                valid_filename = "".join(c for c in degree_name if c.isalnum() or c in (' ', '_')).rstrip()

                # Create the full path for the file
                file_path_html = os.path.join(folder_name, f"{valid_filename}.html")

                # Write the prettified HTML content to a file in the "Fowler" folder
                with open(file_path_html, "w", encoding="utf-8") as f:
                    page_text = coursesoup.prettify()
                    f.write(page_text)
                print(f'Saved: {file_path_html}')

                file_path_txt = os.path.join(folder_name, f"{valid_filename}.txt")

                with open(file_path_txt, "w", encoding="utf-8") as f:
                    f.write(parse_courses(coursesoup))
                print(f'Saved: {file_path_txt}')
        else:
            print("No program list found.")
    else:
        print("No 'Degrees' header found.")


# Main method for convenience and usability
def main():
    
    run_create_troubleshoot = input("Would you like to create the necessary troubleshoot files? y or n: \n")
    print()
    run_parse_header = input("Would you like to create the main html parser? y or n: \n")
    print()

    if run_create_troubleshoot == "y":
        create_troubleshoot()
    
    if run_parse_header == "y":
        parse_college()

main()