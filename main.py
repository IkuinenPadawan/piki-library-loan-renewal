import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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

def find_element_by_name(driver, name):
    return driver.find_element(By.NAME, name)

def insert_to_field(field, input):
    field.send_keys(input)

def click_button(button):
    button.click()

def main():
    driver = setup_driver()
    login(driver, LIBRARY_USERNAME, LIBRARY_PASSWORD)
    driver.quit()

if __name__ == '__main__':
    main()
