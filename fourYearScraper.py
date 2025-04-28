import os
import requests
import re
import csv
from bs4 import BeautifulSoup

home_link = "https://catalog.chapman.edu/content.php?catoid=46&navoid=2411"

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

            if (content.__contains__("B.")):

                degrees.append(degree)

    for i in degrees:

        for sub in i.find_all("a"):

            href = sub["href"]
            parse_degree_page(href)

def parse_degree_page(href):

    complete_url = f"https://catalog.chapman.edu/{href}"

    degree_page = requests.get(complete_url)

    soup = BeautifulSoup(degree_page.content, "html.parser")

    if soup.find("a", string="Suggested"):

        a_tag = soup.find("a", string="Suggested")
        href = a_tag["href"]
        complete_url = f"https://catalog.chapman.edu/{href}"
        parse_planner(complete_url)

    
def parse_planner(url):
    
    planner_page = requests.get(url)

    soup = BeautifulSoup(planner_page.content, "html.parser")

    years = soup.find("div", class_="custom_leftpad_20").find_all("div", class_="acalog-core")

    for year in years:
        
        year_num = year.text.strip()

        year_contents = year.find_next_sibling("ul")

        


def main():

    request_info()

main()