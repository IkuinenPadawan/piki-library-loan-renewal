# PIKI Library Loan Renewal
A Python script that uses Selenium and BeautifulSoup to login to Pirkanmaa library website (https://piki.finna.fi/), retrieve loan information, and renew all loans.

## Table of Contents
-----------------

* [About](#about)
* [Features](#features)
* [Future Features](#future-features)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)


## About
--------

This script is designed to simplify the process of renewing library loans by automating the login, loan retrieval, and renewal processes.

## Features
------------

* Automatically logs in to the library website using a Chrome browser
* Retrieves loan information for all active loans
* Renew all loans with an upcoming due date
* Select loans to be renewed

### Future Features
* Better error handling
* Headless mode
* Renew loans automatically when loans due (check email for loan due reminders)
* Configurations to allow (as far as possible) for usage on different region libraries (all regions have their own website implementations so modifications needed depending on the region)

## Requirements
---------------

### Python and Packages

* Python 3.8+
* Selenium 4.x
* BeautifulSoup 4.x
* Python-dotenv
* Rich
* Chrome based browser

## Installation
--------------

1. Clone the repository: `git clone https://github.com/IkuinenPadawan/piki-library-loan-renewal.git`
2. Create a new file named `.env` in the root directory with your library credentials (see `.env.example`)
3. Install required packages using pip: `pip install -r requirements.txt`

## Usage
--------

1. Run the script using Python: `python main.py`
2. The script will automatically login to the library website, retrieve loan information, ask if user wants loans be renewed and renews all loans
