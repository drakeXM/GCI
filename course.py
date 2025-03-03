# course.py

class Course:
    def __init__(self, name: str, credits: int, prerequisites):
        """Initializes the Course object with a name, credits, and an empty list of courses that require it as a prerequisite."""
        self.name = name
        self.credits = credits
        self.prerequisites = prerequisites

    # def add_prerequisites(self, course_name: str):
    #     """Adds a course to the prerequisites list if it's not already present."""
    #     if course_name not in self.prerequisites:
    #         self.prerequisites.append(course_name)

    def __str__(self):
        """Returns a string representation of the Course object for easy printing."""
        return (f"Course Name: {self.name}\n"
                f"Credits: {self.credits}\n"
                f"Prerequisite For: {', '.join(self.prerequisites) if self.prerequisites else 'None'}")

# Example usage
# course = Course("Introduction to Computer Science", 3)
# course.add_prerequisites("Data Structures")
# course.add_prerequisites("Algorithms")
# print(course)
