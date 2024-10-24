from flask import Flask, render_template

app = Flask(__name__)

user = {
    'name': 'Chris W',
    'id': '2446297',
    'major': 'Electrical Engineer',
    'minor': 'Business',
    'current_year': 'Sophmore',
    'progress': 35  }

# Route for homepage
@app.route('/')
def home():
    percentage_complete = 50  
    return render_template('index.html', percentage=percentage_complete)


@app.route('/courses/<int:year>/<int:semester>')
def courses(year, semester):
    
    courses = get_courses(year, semester)
    return render_template('courses.html', year=year, semester=semester, courses=courses)


def get_courses(year, semester):

    sample_courses = {
        (1, 1): [{'name': 'Calculus 1', 'completed': True}],
        (1, 2): [{'name': 'Calculus 2', 'completed': False}],
        (2, 1): [{'name': 'Multivariable Calculus', 'completed': True}],
        (2, 2): [{'name': 'Electronics and Circuits', 'completed': False}],
        # Add more data as needed for Junior and Senior years.
    }
    return sample_courses.get((year, semester), [])

if __name__ == '__main__':
    app.run(debug=True)

