
from flask import Flask, jsonify, render_template, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Course  # Import your SQLAlchemy models

app = Flask(__name__, static_folder="static")

engine = create_engine('sqlite:///college_plan.db')
Session = sessionmaker(bind=engine)
session = Session()

user = {
    'name': 'Chris W',
    'id': '2446297',
    'major': 'Electrical Engineer',
    'minor': 'Business',
    'current_year': 'Sophmore',
    'progress': 35  }

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/progress")
def progresscircle():
    return render_template("progress/index.html")

@app.route("/freshman") # Make IT TO GO TO FRESHMAN PAGE
def freshman():
    return render_template("freshman/index.html", user = user)

@app.route("/sophomore")
def sophomore():
    return render_template("sophomore/index.html")

@app.route("/junior")
def junior():
    return render_template("junior/index.html")

@app.route('/get_courses')
def get_courses():
    courses = session.query(Course).all()
    course_data = [{
        'id': course.id,
        'class_code': course.class_code,
        'name': course.name
    } for course in courses]
    return jsonify(course_data)



if __name__ == '__main__':
    app.run(debug=True)
