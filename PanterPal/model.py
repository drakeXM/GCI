from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Step 1: Set up the database engine
engine = create_engine('sqlite:///college_plan.db')  # Use SQLite for simplicity
Base = declarative_base()

# Step 2: Define the Majors and Courses tables
class Major(Base):
    __tablename__ = 'majors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(Text)
    total_credits = Column(Integer)  # Add total credits to Major table

class Course(Base):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True)
    class_code = Column(String, nullable=False)
    name = Column(String)
    credits = Column(Integer)
    category = Column(String)  # e.g., "core requirements", "electives"
    major_id = Column(Integer, ForeignKey('majors.id'))

# Step 3: Create the tables in the database
Base.metadata.create_all(engine)

# Step 4: Set up the session
Session = sessionmaker(bind=engine)
session = Session()

# Fetch all class codes from the database
def get_class_codes():
    # Query all courses and select only the class_code
    courses = session.query(Course.class_code).all()

    # Print each class code
    for course in courses:
        print(course.class_code)

# Step 5: Function to insert data from files
def insert_data_from_files(major_name, txt_file_path):
    with open(txt_file_path, 'r') as file:
        lines = file.readlines()

    # Get or create the major
    major = session.query(Major).filter_by(name=major_name).first()
    if major is None:
        major = Major(name=major_name, description='Description for ' + major_name)
        session.add(major)
        session.commit()

    total_credits = 0  # Initialize total credits for the major
    current_category = None

    for line in lines:
        line = line.strip()
        
        # Check for categories (e.g., "lower-division core requirements", "upper-division electives")
        if "requirements" in line.lower() or "electives" in line.lower():
            if not line.startswith("--"):
                current_category = line  # Set the line as the category
                continue  # Skip this line since it's a category label
                
        # Check for course information lines
        if line.startswith("--"):
            parts = line.split(" - ")
            if len(parts) < 2:
                print(f"Could not parse line: {line}")
                continue

            # Extract class code and name
            class_code = parts[0][2:].strip()  # Remove leading "--"
            name = parts[1].split("  ")[0].strip()  # Extract only the name part
            
            # Extract credits (assuming credits are always mentioned at the end)
            credit_part = line.split()[-2]  # This should be the credit value
            try:
                credits = int(credit_part)  # Convert credit to integer
            except ValueError:
                print(f"Could not parse credits for course: {class_code}. Line: {line}")
                continue

            # Create the course with the extracted category type
            course = Course(class_code=class_code, name=name, credits=credits, category=current_category, major_id=major.id)
            session.add(course)
            total_credits += credits  # Update total credits

    session.commit()

    # Update total credits in the major record
    major.total_credits = total_credits
    session.commit()
    
    print(f"Data inserted for {major_name}. Total credits: {total_credits}")

# Function to check and print the data in the database, grouped by major and category
def check_data_grouped_by_major_and_category():
    # Query all majors
    majors = session.query(Major).all()
    print("Majors and their Courses Grouped by Category:")

    for major in majors:
        # Print major information
        print(f"\nMajor ID: {major.id}, Name: {major.name}, Description: {major.description}")
        
        # Query courses related to this major
        courses = session.query(Course).filter_by(major_id=major.id).all()

        # Group courses by category
        categories = {}
        for course in courses:
            # Initialize category list if it doesn't exist
            if course.category not in categories:
                categories[course.category] = []
            # Append the course to its category
            categories[course.category].append(course)
        
        # Print courses for each category under the current major
        if categories:
            for category, courses in categories.items():
                print(f"  Category: {category}")
                for course in courses:
                    print(f"    - ID: {course.id}, Class Code: {course.class_code}, Name: {course.name}, Credits: {course.credits}")
        else:
            print("  No courses found for this major.")

# Main script to process and display everything
if __name__ == "__main__":
    majors_folder = 'Fowler'  # Adjusted to point to the Fowler folder
    for major_file in os.listdir(majors_folder):
        if major_file.endswith('.txt'):  # Only process text files
            major_name = major_file.replace('.txt', '')  # Get the major name without the extension
            txt_file_path = os.path.join(majors_folder, major_file)  # Path to the text file
            insert_data_from_files(major_name, txt_file_path)

    # After all data is inserted, we can check grouped data and class codes
    check_data_grouped_by_major_and_category()
    get_class_codes()  # Optional: If you want to display class codes after the insert
