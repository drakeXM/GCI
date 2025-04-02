import os
import csv

# Create directory for finished output file
def init_dir(dir_name):
    valid_path = os.getcwd() + '\\' + dir_name
    try:
        os.mkdir(dir_name)
    except Exception as e:
        print("Error creating directory:", e)

def search_dir():
    rows = [["Major", "Course Name", "Credits", "Prerequisites", "Category"]]
    dirs = os.listdir(os.getcwd() + '\\Output')
    for dir in dirs:
        new_rows = read_file(rows, dir)
        rows = new_rows
    return rows

def read_file(rows, dir):
    file_path = os.getcwd() + "\\Output\\" + dir 
    with open(file_path, "r", encoding="utf-8", newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] != "Course Name":
                dir = dir.removesuffix(".csv")
                print(dir)
                new_row = [f"{dir}"] + row
                rows.append(new_row)
    return rows
    
def write_file(rows):
    file_path = os.getcwd() + "\\sorted\\majors.csv"
    with open(file_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)    

def main():
    init_dir("sorted")
    rows = search_dir()
    write_file(rows)

main()