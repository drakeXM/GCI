import requests
import re
import csv
from bs4 import BeautifulSoup

home_link = "https://catalog.chapman.edu/content.php?catoid=46&navoid=2411"
all_course_data = []
current_major = ""
num_degrees = 0
num_degree_links = 0
links_searched = []
test_page = ""
is_test_page = True

# Get request from website
def request_info():
    catalog_page = requests.get(home_link)
    soup = BeautifulSoup(catalog_page.content, "html.parser")
    consolidate(soup)

# Sort out all degrees
def consolidate(souObj):
    # Finds the main body of the page
    page_body = souObj.find("td", class_="block_content")
    degrees = []

    for sub in page_body.find_all("ul"):
        for degree in sub.find_all("li"):
            content = degree.text.strip()
            if "B." in content:
                global num_degrees
                num_degrees += 1
                degrees.append(degree)

    for degree_element in degrees:
        degree_link = degree_element.find("a")
        if degree_link and degree_link.has_attr("href"):
            global num_degree_links
            num_degree_links += 1
            global current_major
            current_major = degree_element.text.split("(")[0].strip()
            href = degree_link["href"]
            parse_degree_page(href)

def parse_degree_page(href):
    global links_searched
    complete_url = f"https://catalog.chapman.edu/{href}"
    degree_page = requests.get(complete_url)
    if degree_page:
        global is_test_page
        global test_page
        soup = BeautifulSoup(degree_page.content, "html.parser")
        if is_test_page:
            test_page = soup.prettify()
            is_test_page = False
        suggested_link = soup.find("a", string=re.compile(r"Suggested.*Plan", re.IGNORECASE))
        if suggested_link and suggested_link.has_attr("href"):
            href = suggested_link["href"]
            complete_url = f"https://catalog.chapman.edu/{href}"
            links_searched.append(complete_url)
            parse_planner(complete_url)
        elif suggested_link:
            print(suggested_link.prettify())
        else:
            links_searched.append("Unable to request planner page")
    else: 
        print("unable to request degree page")
    

def parse_planner(url):
    print(f"--- Parsing Planner URL: {url} ---")
    planner_page = requests.get(url)
    soup = BeautifulSoup(planner_page.content, "html.parser")

    # Find the div that wraps the planner
    planner_container = soup.find("div", class_="custom_leftpad_20")
    if planner_container:
        print("Planner container found.")
        # Find all divs with class "acalog-core"
        core_divs = planner_container.find_all("div", class_="acalog-core")
        print(f"Found {len(core_divs)} core divs.")

        for div in core_divs:
            h2_tag = div.find("h2")
            if h2_tag:
                print(f"Found h2 tag: {h2_tag.text}")
                year_match = re.search(r"Year\s*(\d)", h2_tag.text, re.IGNORECASE)
                year = year_match.group(1) if year_match else None
                if year:
                    print(f"Extracted year: {year}")
                    ul_tag = h2_tag.find_next_sibling("ul")
                    if ul_tag:
                        print("Found ul tag following h2.")
                        semester = None
                        for item in ul_tag.find_all("li"):
                            strong_tag = item.find("strong")
                            if strong_tag:
                                semester_match = re.search(r"(Fall|Spring)\s*Semester", strong_tag.text, re.IGNORECASE)
                                semester = semester_match.group(1) if semester_match else semester
                                if semester and item.find("a"):
                                    print(f"Found semester: {semester}")
                                    a_tag = item.find("a")
                                    class_name = a_tag.text.split(" - ")[0].strip()
                                    print(f"Found class: {class_name}")
                                    if current_major and year and semester and class_name:
                                        print(f"Appending data: {current_major}, {year}, {semester}, {class_name}")
                                        global all_course_data
                                        all_course_data.append([current_major, year, semester, class_name])
                                    else:
                                        print(f"Warning: Missing data for class: {current_major=}, {year=}, {semester=}, {class_name=}")
                    else:
                        print("No ul tag found following h2.")
            else:
                print("No h2 tag found in core div.")
    else:
        print(f"Warning: Planner container not found at {url}")

def save_to_csv():
    filename = "plannerTemplate.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["major", "year", "semester", "class name"])  # Write header row
        csv_writer.writerows(all_course_data)
    print(f"Data saved to {filename}")

def troubleshoot():
    log_filename = "logs.txt"
    global num_degrees
    global num_degree_links
    global links_searched
    global test_page
    with open(log_filename, 'w', encoding="utf-8") as log_file:
        log_file.write(f"Number of degrees found: {num_degrees}\n")
        log_file.write(f"Number of degrees with links: {num_degree_links}\n")
        log_file.write(f"Links searched: {links_searched}\n")
        log_file.write(f"test page: {test_page}")
    print(f"Troubleshooting log written to {log_filename}")

def main():
    request_info()
    save_to_csv()
    # troubleshoot()

if __name__ == "__main__":
    main()