# Assignment 2 Documentation and Instructions

## Introduction
This project implements a web application for course scheduling using Flask and provides end-to-end (E2E) tests using Selenium and unit tests using the `unittest` framework. The goal is to ensure that the course scheduling solution handles various edge cases and correctly identifies cyclic dependencies.

## Project Structure
The project consists of the following files:
- `app.py`: The Flask web application that provides a web interface for inputting the number of courses and prerequisites.
- `index.html`: The HTML template for the web interface.
- `solution.py`: The Python module containing the `Solution` class with the `findOrder` method for determining the course schedule.
- `test_app.py`: The test suite containing E2E tests and unit tests for the application and solution.

## Instructions
1. **Set up the virtual environment and install dependencies**:
   ```sh
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt


2. Run the Flask application:

    python app.py

3. Run the test suite with coverage:

     coverage run --source=app,solution -m unittest discover
     coverage report -m
     coverage html


 4. Access the application:
    Open a web browser and go to http://127.0.0.1:5000/.  



See full documentation for more deatils