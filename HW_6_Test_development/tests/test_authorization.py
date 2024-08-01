import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from dotenv import load_dotenv

load_dotenv()

LOGIN_FIELD_ID = "passp-field-login"
SUBMIT_BUTTON_ID = "passp:sign-in"
PASSWORD_FIELD_ID = "passp-field-passwd"
LOGIN_HINT_ID = "field:input-login:hint"
PASSWORD_HINT_ID = "field:input-passwd:hint"
CURRENT_ACCOUNT_CLASS = "CurrentAccount-displayName"
MIN_DELAY_SEC = 1.5
MAX_DELAY_SEC = 3.0
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")


class TestYandexAuthorization:
    def setup_method(self):
        self.login = LOGIN
        self.false_login = 'sdfjk13ldkng'
        self.password = PASSWORD
        self.false_password = 'lskdhg02i2n'
        self.browser = webdriver.Chrome()
        self.browser.get("https://passport.yandex.ru/auth")
        self.input_login_field = self.browser.find_element(By.ID, LOGIN_FIELD_ID)
        if self.input_login_field.text:
            self.input_login_field.send_keys("")
            sleep(MIN_DELAY_SEC)

    def teardown_method(self):
        self.browser.quit()

    def test_false_login(self):
        self.input_login_field.send_keys(self.false_login)
        self.browser.find_element(By.ID, SUBMIT_BUTTON_ID).click()
        sleep(MAX_DELAY_SEC)
        input_field_hint = self.browser.find_element(By.ID, LOGIN_HINT_ID)
        if input_field_hint:
            assert input_field_hint.text.strip() == "Нет такого аккаунта. Проверьте логин или войдите по телефону"

    def test_true_login(self):
        self.input_login_field.send_keys(self.login)
        self.browser.find_element(By.ID, SUBMIT_BUTTON_ID).click()
        sleep(MAX_DELAY_SEC)
        current_account_name = self.browser.find_element(By.CLASS_NAME, CURRENT_ACCOUNT_CLASS).text
        assert current_account_name.strip() == self.login

    def test_empty_login(self):
        self.input_login_field.send_keys("")
        self.browser.find_element(By.ID, SUBMIT_BUTTON_ID).click()
        sleep(MAX_DELAY_SEC)
        login_field_hint = self.browser.find_element(By.ID, LOGIN_HINT_ID)
        if login_field_hint:
            assert login_field_hint.text.strip() == "Логин не указан"

    def test_password(self):
        self.input_login_field.send_keys(self.login)
        self.browser.find_element(By.ID, SUBMIT_BUTTON_ID).click()
        sleep(MAX_DELAY_SEC)
        current_account_name = self.browser.find_element(By.CLASS_NAME, CURRENT_ACCOUNT_CLASS).text
        assert current_account_name.strip() == self.login
        input_password_field = self.browser.find_element(By.ID, PASSWORD_FIELD_ID)
        input_password_field.send_keys(self.false_password)
        self.browser.find_element(By.ID, SUBMIT_BUTTON_ID).click()
        sleep(MAX_DELAY_SEC)
        password_field_hint = self.browser.find_element(By.ID, PASSWORD_HINT_ID)
        if password_field_hint:
            assert password_field_hint.text.strip() == "Неверный пароль"
            sleep(MIN_DELAY_SEC)
        input_password_field.send_keys("")
        self.browser.find_element(By.ID, SUBMIT_BUTTON_ID).click()
        sleep(MAX_DELAY_SEC)
        password_field_hint = self.browser.find_element(By.ID, PASSWORD_HINT_ID)
        if password_field_hint:
            assert password_field_hint.text.strip() == "Пароль не указан"
            sleep(MIN_DELAY_SEC)
