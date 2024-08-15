# Plant Growth Tracker

## Overview

The Plant Growth Tracker is a web application built with Flask that allows users to track the growth of their plants over time. The app enables users to add new plant entries, upload photos, and visualize plant growth through interactive charts. The growth data is displayed both numerically and graphically, providing insights into plant development.

## Features

- **Add Plant Entries:** Users can input plant details, including name, date, height, notes, and upload a photo.
- **View Growth Progress:** Displays a line chart showing plant height over time.
- **Timeline of Entries:** Lists all plant entries with their growth details and uploaded photos.
- **Responsive Design:** Utilizes Bootstrap for a clean and responsive interface.


## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/chandranshulg/PLANT-GROWTH-TRACKER.git
   cd PLANT-GROWTH-TRACKER

2. **Set Up the Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install Dependencies**

      ```bash
     pip install -r requirements.txt
     
4. **Create the Database**

    ```bash

    python
    >>> from app import db
    >>> db.create_all()
    >>> exit()
5. **Run the Application**

   ```bash
   python app.py
The application will be available at http://127.0.0.1:5000.

## Usage

1. **Adding a Plant Entry**

Navigate to the home page and fill out the form to add a new plant entry.

Upload a photo if available and submit the form.

2. **Viewing Growth Progress**

The growth chart on the home page visualizes the height of plants over time.

3. **Viewing Plant Timeline**

All plant entries are listed with their details, including photos and notes.

## Code Structure

**app.py**: The main Flask application file containing routes, database setup, and logic.
**requirements.txt**: List of Python dependencies required for the application.

## Dependencies

The application requires the following Python packages:

Flask
Flask-SQLAlchemy
pandas
plotly
Install these dependencies using the requirements.txt file.


