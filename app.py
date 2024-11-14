
from flask import Flask, render_template, url_for

app = Flask(__name__, static_folder="static")

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





if __name__ == '__main__':
    app.run(debug=True)

