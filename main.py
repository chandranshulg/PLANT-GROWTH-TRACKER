import os
from flask import Flask, render_template_string, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import plotly.graph_objs as go
import pandas as pd

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Set up the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Plant model
class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(100), nullable=True)
    date = db.Column(db.String(10), nullable=False)
    height = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text, nullable=True)

# Initialize the database
db.create_all()

# HTML template as a string
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plant Growth Tracker</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <div class="container">
        <h1 class="mt-5 text-center">Plant Growth Tracker</h1>
        <form action="/add" method="POST" enctype="multipart/form-data">
            <div class="form-group">
                <label for="name">Plant Name</label>
                <input type="text" class="form-control" id="name" name="name" required>
            </div>
            <div class="form-group">
                <label for="date">Date</label>
                <input type="date" class="form-control" id="date" name="date" required>
            </div>
            <div class="form-group">
                <label for="height">Height (cm)</label>
                <input type="number" step="0.1" class="form-control" id="height" name="height" required>
            </div>
            <div class="form-group">
                <label for="notes">Notes</label>
                <textarea class="form-control" id="notes" name="notes"></textarea>
            </div>
            <div class="form-group">
                <label for="photo">Photo</label>
                <input type="file" class="form-control-file" id="photo" name="photo">
            </div>
            <button type="submit" class="btn btn-primary">Add Entry</button>
        </form>
        <hr>
        <h2 class="mt-5">Growth Progress</h2>
        <div id="growth-chart"></div>
        <hr>
        <h2 class="mt-5">Growth Timeline</h2>
        <ul class="list-group">
            {% for plant in plants %}
                <li class="list-group-item">
                    <strong>{{ plant.name }}</strong> ({{ plant.date }}): 
                    Height: {{ plant.height }} cm
                    {% if plant.photo %}
                        <br><img src="{{ url_for('static', filename='uploads/' + plant.photo) }}" width="150">
                    {% endif %}
                    <br>Notes: {{ plant.notes }}
                </li>
            {% endfor %}
        </ul>
    </div>
    <script>
        var data = {{ growth_data | safe }};
        var layout = {
            title: 'Plant Growth Over Time',
            xaxis: { title: 'Date' },
            yaxis: { title: 'Height (cm)' }
        };
        Plotly.newPlot('growth-chart', data, layout);
    </script>
</body>
</html>
'''

# Home route
@app.route('/')
def index():
    plants = Plant.query.order_by(Plant.date).all()
    growth_data = []

    if plants:
        df = pd.DataFrame([(plant.date, plant.height) for plant in plants], columns=['Date', 'Height'])
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values(by='Date')

        growth_data = [
            go.Scatter(
                x=df['Date'],
                y=df['Height'],
                mode='lines+markers',
                name='Height'
            )
        ]

    return render_template_string(html_template, plants=plants, growth_data=growth_data)

# Route to add a new plant entry
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    date = request.form['date']
    height = float(request.form['height'])
    notes = request.form['notes']
    photo = None

    if 'photo' in request.files and request.files['photo'].filename != '':
        photo_file = request.files['photo']
        photo_filename = secure_filename(photo_file.filename)
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
        photo_file.save(photo_path)
        photo = photo_filename

    new_plant = Plant(name=name, date=date, height=height, notes=notes, photo=photo)
    db.session.add(new_plant)
    db.session.commit()

    flash('Plant entry added successfully!')
    return redirect(url_for('index'))

# Start the Flask app
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
