import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from enum import Enum

class RenewConfirmation(Enum):
    YES = 'y'
    NO = 'n'

load_dotenv()
LIBRARY_USERNAME = os.getenv("LIBRARY_USERNAME")
LIBRARY_PASSWORD = os.getenv("LIBRARY_PASSWORD")

def setup_driver():
    options = Options()
    return webdriver.Chrome(options=options)

def login(driver, username, password):
    driver.get("https://piki.finna.fi/MyResearch/UserLogin")

    username_field = find_element_by_name(driver, "username")
    password_field = find_element_by_name(driver, "password")

    insert_to_field(username_field, username)
    insert_to_field(password_field, password)

    click_button(find_element_by_name(driver, "processLogin"))

def print_loan_details(driver):
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'table.myresearch-table'))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    loans_table = soup.find("table", {"class": "myresearch-table"})

    for loan in loans_table.find_all("tr")[1:]:
        title_column = loan.find("div", {"class": "title-column"}).text.strip()
        status_column = loan.find("div", {"class": "status-column"}).text.strip()

        print(f"Title: {title_column}")
        print(f"Status: {status_column}")

def ask_renew_all_loans(driver):
    if not get_user_confirmation():
        return

    renew_all_button = find_element_by_name(driver, "renewAll")
    click_button(renew_all_button)

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "confirm_renew_all_yes")))
    confirm_button = driver.find_element(By.ID, "confirm_renew_all_yes")
    click_button(confirm_button)

def get_user_confirmation():
    while True:
        user_input = input("Renew all loans? ({} / {})".format(RenewConfirmation.YES.value, RenewConfirmation.NO.value))
        if user_input.strip() == RenewConfirmation.YES.value:
            return True
        elif user_input.strip() == RenewConfirmation.NO.value:
            return False
        else:
            print(f"Invalid input: '{user_input}'. Please enter either '{RenewConfirmation.YES.value}' or '{RenewConfirmation.NO.value}'")

def find_element_by_name(driver, name):
    return driver.find_element(By.NAME, name)

def insert_to_field(field, input):
    field.send_keys(input)

def click_button(button):
    button.click()

def main():
    driver = setup_driver()
    login(driver, LIBRARY_USERNAME, LIBRARY_PASSWORD)
    print_loan_details(driver)
    ask_renew_all_loans(driver)
    print_loan_details(driver)
    driver.quit()

if __name__ == '__main__':
    main()
