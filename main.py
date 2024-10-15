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

    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")

    username_field.send_keys(username)
    password_field.send_keys(password)

    login_button = driver.find_element(By.NAME, "processLogin")
    login_button.click()


def main():
    driver = setup_driver()
    login(driver, LIBRARY_USERNAME, LIBRARY_PASSWORD)
    driver.quit()

if __name__ == '__main__':
    main()
