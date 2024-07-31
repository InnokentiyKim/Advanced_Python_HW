import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from dotenv import load_dotenv

load_dotenv()

LOGIN_FIELD_ID = "passp-field-login"
SUBMIT_BUTTON_ID = "passp:sign-in"
PASSWORD_FIELD_ID = "passp-field-passwd"
DELAY_SEC = 3
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")

def authorize(login, password):
    browser = webdriver.Chrome()
    browser.get("https://passport.yandex.ru/auth")
    input_login_field = browser.find_element(By.ID, LOGIN_FIELD_ID).send_keys(login)
    login_submit_button = browser.find_element(By.ID, SUBMIT_BUTTON_ID).click()
    sleep(DELAY_SEC)
    input_password_field = browser.find_element(By.ID, PASSWORD_FIELD_ID).send_keys(password)
    password_submit_button = browser.find_element(By.ID, SUBMIT_BUTTON_ID).click()
    sleep(DELAY_SEC)
    browser.quit()