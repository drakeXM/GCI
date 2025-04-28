Hello! Welcome to the rough rough rough draft of Panther Pal. A 4-year planning tool.

## Progress so far ##

1) Handler - Main web scraping application
2) file_seive - Consolidates the data collected from handler into an excel spreadsheet which can be interpreted by the google site
3) Course - Object definition
4) PanterPal - The SQL database implementation
5) PantherPal - The main web frontend
6) fourYearScraper - Scrapes the suggested 4 year plan made by the university for each major

## IMPORTANT NOTES FOR USE ##

- When running Handler, fourYearScraper, and file_seive, it is advised to first initialize a virtual environment and install the necessary packages in said environment. The necessary requirements may be installed using requirements.txt
- MAKE SURE THAT YOU'RE AWARE OF YOUR WORKING DIRECTORY!!! If you're unsure of your directory, you can see your filepath in the powershell terminal. If you're not convinced by that, you can also run print(os.getcwd()) in a python script to see where your interpreter thinks your working directory is. (don't forget to install os with import os)
- You must install several packages for the script to run. after youve initialized your venv, you'll be prompted to install from requirements.txt
