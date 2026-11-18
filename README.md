# Course Schedule Web App and E2E Tests

A Flask application that computes a course order from a course count and a list of prerequisite pairs. The repository uses the app to demonstrate browser-based testing with Selenium.

## Features

- Submit prerequisites through a web form and view the resulting order.
- Detect circular dependencies with a depth-first search.
- Exercise the form with Selenium and check the solver with Python's `unittest`.

## Getting Started

Install Python 3 and Chrome, then run the following from the repository root. Use the app locally with trusted input because the form evaluates prerequisite expressions.

```sh
python -m pip install -r requirements.txt
python app.py
```

With Flask running at `http://127.0.0.1:5000/`, run `python -m unittest discover -v` in a separate terminal. The browser tests use Chrome and download ChromeDriver through webdriver-manager.

See [the original assignment instructions](README.md.txt) for the coverage commands.
