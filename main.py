import time
import os
import logging
import sys
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from enum import Enum
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

class RenewConfirmation(Enum):
    YES = 'y'
    NO = 'n'

load_dotenv()
LIBRARY_USERNAME = os.getenv("LIBRARY_USERNAME")
LIBRARY_PASSWORD = os.getenv("LIBRARY_PASSWORD")

console = Console()

def setup_driver():
    try:
        options = Options()
        return webdriver.Chrome(options=options)
    except Exception as e:
        logging.error(f"Failed to setup driver: {e}")
        exit(1)

def login(driver, username, password):
    try:
        driver.get("https://piki.finna.fi/MyResearch/UserLogin")

        username_field = find_element_by_name(driver, "username")
        password_field = find_element_by_name(driver, "password")

        insert_to_field(username_field, username)
        insert_to_field(password_field, password)

        click_button(find_element_by_name(driver, "processLogin"))
    except Exception as e:
        logging.error(f"Failed to log in: {e}")
        exit(1)

def print_loan_details(driver):
    try:
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'table.myresearch-table'))
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        loans_table = soup.find("table", {"class": "myresearch-table"})

        loan_table = build_loan_detail_table(loans_table)
        console.print(loan_table)

    except Exception as e:
        logging.error(f"Failed to print loan details: {e}")


def renew_all_loans(driver):
    try:
        renew_all_button = find_element_by_name(driver, "renewAll")
        if not renew_all_button:
            sys.exit(0)
        click_button(renew_all_button)

        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "confirm_renew_all_yes")))
        confirm_button = driver.find_element(By.ID, "confirm_renew_all_yes")
        click_button(confirm_button)
    except Exception as e:
        console.print("Loans cannot be renewed", style="red")
        sys.exit(0)

def ask_if_renew_all_or_some():
        try:
            renew_all = Prompt.ask(
                "Renew all loans? y(es) | n(o) to Select loans to be renewed" , 
                choices=[RenewConfirmation.YES.value, RenewConfirmation.NO.value],
            )
            match renew_all:
                case RenewConfirmation.YES.value:
                    return True
                case RenewConfirmation.NO.value:
                    return False
        except Exception as e:
            logging.error(f"Failed to get user confirmation: {e}")

def find_element_by_name(driver, name):
    return driver.find_element(By.NAME, name)

def insert_to_field(field, input):
    field.send_keys(input)

def click_button(button):
    button.click()

def renew_some_loans(driver):
    rows = driver.find_elements(By.CSS_SELECTOR, "tr.myresearch-row")

    checkboxes = {}

    for index, row in enumerate(rows, start=1):
        try:
            if row.get_attribute("aria-hidden") == "true":
                continue

            try:
                title_element = row.find_element(By.CSS_SELECTOR, "a.record-title")
                title = title_element.text
                checkbox = row.find_element(By.CSS_SELECTOR, "input.checkbox-select-item")
                checkboxes[index] = (title, checkbox)
                print(f"{index}: {title}")
            except NoSuchElementException:
                logging.warning(f"Skipping a row without a checkbox or book")
                continue

        except Exception as e:
            logging.error(f"Skipping a row due to error: {e}")
            logging.error(f"Row HTML: {row.get_attribute('outerHTML')}")

    if not checkboxes:
        console.print("No loans can be renewed", style="red")
        sys.exit(0)

    console.print("Available options to select:", style="bold")
    choices = input("\nEnter the numbers of the books you want to renew, separated by commas: ")

    selected_indices = [int(num.strip()) for num in choices.split(",") if num.strip().isdigit()]
    for index in selected_indices:
        if index in checkboxes:
            title, checkbox = checkboxes[index]
            driver.execute_script("arguments[0].scrollIntoView();", checkbox)  
            checkbox.click()
            print(f"Checked: {title}")
        else:
            print(f"Invalid selection: {index}")

    confirm = input("\nConfirm renewal(s)? (y/n): ")

    if confirm.lower() == "y":
        try:
            dropdown_toggle = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "renewSelected"))
            )
            dropdown_toggle.click()

            confirm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "confirm_renew_selected_yes"))
            )
            click_button(confirm_button)
            print("Selected loans renewed!")
        except Exception as e:
            logging.error(f"Failed to renew selected: {e}")

def build_loan_detail_table(loan_table):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Title")
    table.add_column("Author") 
    table.add_column("Status", justify="right")


    for loan in loan_table.find_all("tr")[1:]:
        status_column = loan.find("div", {"class": "status-column"}).text.strip()
        record_title = loan.find("a", {"class": "record-title"}).text.strip()
        record_author = loan.find("span", {"class": "authority-label"}).text.strip()

        table.add_row(
            record_title, record_author, status_column
        )

    return table

def main():
    try:
        driver = setup_driver()
        login(driver, LIBRARY_USERNAME, LIBRARY_PASSWORD)
        print_loan_details(driver)
        renew_all = ask_if_renew_all_or_some()
        if renew_all:
            renew_all_loans(driver)
        else:
            renew_some_loans(driver)
        time.sleep(3)
        print_loan_details(driver)
    except Exception as e:
        logging.error(f"Failed to run the loan renewal script: {e}")
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
