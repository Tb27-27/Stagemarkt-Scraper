## Keuzedeel Solliciteren Automator

This Python script automates the process of gathering job vacancy details for your "Keuzedeel Solliciteren" assignment. Instead of copying and pasting everything manually, this tool scrapes the data from Stagemarkt (and similar platforms) and generates a perfectly formatted Markdown report.

---

### Features
Automatic Extraction: Pulls job titles, contact persons, emails, and phone numbers.

Smart Parsing: Uses JSON-LD and Regex to find contact details.

Markdown Output: Generates a .md file named specifically for your submission (including your name and student number).

Refinement: Includes placeholders for your personal reflection and recognition codes.

---

### Getting Started

#### 1. Prerequisites
Make sure you have Python 3.7+ installed on your machine.

#### 2. Installation
First, clone or download this folder. Then, install the required dependencies using the requirements.txt file:


```bash
pip install -r requirements.txt
```

#### 3. Running the Script
Start the script by running:


```bash
python "Solicitatie Automaat UwU.py"
```

---

## How to Use

##### Enter Your Details: 
    The script will ask for your Student Number and Full Name.
    Everything is run locally, so this won't be used for anything except

##### Paste URLs: Copy the URL of a vacancy from Stagemarkt and paste it into the terminal.

 > https://stagemarkt.nl

##### example url:

```
https://stagemarkt.nl/stages/software-developer_0d1c5c9b-7c2a-4aab-a80d-a86c957ac446-25998?niveau=4&type=1&range=10&crebocode=25998&plaatsPostcode=Amsterdam
```

##### Repeat: You can add up to 8 vacancies (or type stop to finish early).

Check Output: A file named Keuzedeel Solliciteren [Number] [Name].md will appear in your folder.

---

## Dependencies

##### requests: 
* For fetching the webpage data.

##### beautifulsoup4: 
* For parsing the HTML content.

##### Note: 
* This tool is intended to help organize your research.
* Make sure to double-check the scraped data and fill in the "Reflectie" sections manually before submitting!