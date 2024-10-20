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

    click_button(driver.find_element(By.NAME, "processLogin"))

def print_loan_details(driver):
    # Wait for 10 seconds for the table to be visible on the page
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'table.myresearch-table'))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    title_column = soup.find_all('div', {'class': 'title-column'})
    status_column = soup.find_all('div', {'class': 'status-column'})

    if len(title_column) == len(status_column):
        for title, status in zip(title_column, status_column):
            print(title.text.strip())
            print(status.text.strip())

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
    driver.quit()

if __name__ == '__main__':
    main()
