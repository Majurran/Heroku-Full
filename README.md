# Elderly Wellbeing Web App

## Setup & Installation

Make sure you have the latest version of Python installed.

```bash
git clone <repo-url>
```

Important! Make sure you are in a Python Virtual Environment before using pip install.

For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

For Mac and Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

Once you are in the virtual environment, install the packages:
```bash
pip install -r requirements.txt
```

## Running The App

```bash
python main.py
```

## Viewing The App

Go to `http://127.0.0.1:5000`


## (Optional) djLint Formatter 
Using the Prettier formatter messes up the Jinja2 format in the HTML files.
You can use djLint to format the HTML pages with Jinja2.
djLint documentation: https://djlint.com/docs/formatter/

To review what may change in formatting run:
```bash
djlint . --check
```

To format the code and update files run:
```bash
djlint . --reformat
```