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
    with open("raw.txt", "w", encoding="utf-8") as f:
        f.write(text)

    with open("links.txt", "w", encoding="utf-8") as f:
        for link in soup.find_all('a'):
            linkString = link.get('href')
            f.write(f"{linkString}\n")

def parse_header():
    
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
                subsoup = BeautifulSoup(degree_response.content, "html.parser")

                # Clean the degree name to make it a valid filename
                valid_filename = "".join(c for c in degree_name if c.isalnum() or c in (' ', '_')).rstrip()

                # Create the full path for the file
                file_path = os.path.join(folder_name, f"{valid_filename}.html")

                # Write the prettified HTML content to a file in the "Fowler" folder
                with open(file_path, "w", encoding="utf-8") as f:
                    page_text = subsoup.prettify()
                    f.write(page_text)

                print(f'Saved: {file_path}')
        else:
            print("No program list found.")
    else:
        print("No 'Degrees' header found.")

# Main method for convenience and usability
def main():
    
    run_create_troubleshoot = input("Would you like to create the necessary troubleshoot files? y or n: ")
    run_parse_header = input("Would you like to create the main html parser? y or n: ")

    if run_create_troubleshoot == "y":
        create_troubleshoot()
    
    if run_parse_header == "y":
        parse_header()

main()