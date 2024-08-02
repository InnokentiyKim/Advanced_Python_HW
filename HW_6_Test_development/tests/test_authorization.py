import os
import pytest
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
PHONE_CODE_ID = "passp-field-phoneCode"

MIN_DELAY_SEC = 1.5
MAX_DELAY_SEC = 3.0

LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
FALSE_PASSWORD = PASSWORD + '1'


class TestYandexAuthorization:
    """
    Класс для тестирования авторизации на Яндекс ID.
    """
    def setup_method(self):
        """
        Setup метод. Инициализирует веб-драйвер Chrome, переходит на страницу аутентификации
        Яндекса и получает поле ввода логина. Если поле ввода логина не пустое, оно очищается и ожидается минимальная
        задержка.
        """
        self.browser = webdriver.Chrome()
        self.browser.get("https://passport.yandex.ru/auth")
        self.input_login_field = self.browser.find_element(By.ID, LOGIN_FIELD_ID)
        if self.input_login_field.text:
            self.input_login_field.send_keys("")
            sleep(MIN_DELAY_SEC)

    def teardown_method(self):
        """
        Teardown метод. Метод очистки, который закрывает браузер после каждого теста.
        Этот метод вызывается после каждого теста в классе тестов.
        """
        self.browser.quit()

    @pytest.mark.parametrize(
        "login,expected",
        [
            ("ierhgit93jpweojt", "Нет такого аккаунта. Проверьте логин или войдите по телефону"),
            ("ва#!", "Такой логин не подойдет"),
            ("", "Логин не указан"),
        ],
        ids=[1, 2, 3]
    )
    def test_false_login(self, login, expected):
        """
        Тестирование сценария неправильного логина.
        Эта функция использует декоратор `@pytest.mark.parametrize`, чтобы определить несколько тестовых случаев
        с различными значениями логина и ожидаемыми сообщениями об ошибке.
        Она отправляет значение логина в поле ввода логина, нажимает кнопку отправки, ожидает максимальное время
        задержки, а затем проверяет, соответствует ли подсказка поля ввода ожидаемому сообщению об ошибке.
        Если подсказка поля ввода найдена и текст совпадает с ожидаемым сообщением об ошибке, тест проходит.
        В противном случае он завершается с информативным сообщением об ошибке.
        Параметры:
            login (str): Значение логина для тестирования.
            expected (str): Ожидаемое сообщение об ошибке для данного значения логина.
        """
        self.input_login_field.send_keys(login)
        self.browser.find_element(By.ID, SUBMIT_BUTTON_ID).click()
        sleep(MAX_DELAY_SEC)
        input_field_hint = self.browser.find_element(By.ID, LOGIN_HINT_ID)
        if input_field_hint:
            assert input_field_hint.text.strip() == expected, f"Failed in test_false_login. Case with login: {login}"

    def test_true_login(self):
        """
        Тестирование сценария правильного логина. Функция вводит правильные данные для входа и проверяет,
        что текущее имя аккаунта соответствует ожидаемому значению.
        Функция отправляет данные для входа в поле ввода, нажимает кнопку отправки,
        ждет максимальное время задержки и затем извлекает текущее имя аккаунта с веб-страницы.
        """
        self.input_login_field.send_keys(LOGIN)
        self.browser.find_element(By.ID, SUBMIT_BUTTON_ID).click()
        sleep(MAX_DELAY_SEC)
        current_account_name = self.browser.find_element(By.CLASS_NAME, CURRENT_ACCOUNT_CLASS).text
        assert current_account_name.strip() == LOGIN

    @pytest.mark.parametrize(
        "password,expected",
        [
            (FALSE_PASSWORD, "Неверный пароль"),
            ("", "Пароль не указан"),
        ],
        ids=[1, 2]
    )
    def test_false_password(self, password, expected):
        """
        Тестирование сценария неправильного пароля.
        Эта функция использует декоратор `@pytest.mark.parametrize`,
        чтобы определить несколько тестовых случаев с различными значениями пароля и ожидаемыми сообщениями об ошибке.
        Она отправляет верное значение логина в поле ввода логина, нажимает кнопку отправки, ожидает максимальное
        время задержки. Затем отправляет значение пароля в поле ввода пароля и нажимает кнопку отправки.
        Если подсказка поля ввода пароля найдена и текст совпадает с ожидаемым сообщением об ошибке, тест проходит.
        В противном случае он завершается с информативным сообщением об ошибке.
        Параметры:
            password (str): Значение пароля для тестирования.
            expected (str): Ожидаемое сообщение об ошибке для данного значения пароля.
        """
        self.input_login_field.send_keys(LOGIN)
        self.browser.find_element(By.ID, SUBMIT_BUTTON_ID).click()
        sleep(MAX_DELAY_SEC)
        input_password_field = self.browser.find_element(By.ID, PASSWORD_FIELD_ID)
        input_password_field.send_keys(password)
        self.browser.find_element(By.ID, SUBMIT_BUTTON_ID).click()
        sleep(MAX_DELAY_SEC)
        password_field_hint = self.browser.find_element(By.ID, PASSWORD_HINT_ID)
        if password_field_hint:
            assert password_field_hint.text.strip() == expected, (f"Failed in test_false_password. "
                                                                  f"Case with password: {password}")
            sleep(MIN_DELAY_SEC)

    def test_true_password(self):
        """
        Тестирование сценария правильного пароля. Функция отправляет верное значение логина в поле ввода логина,
        нажимает кнопку отправки, ожидает максимальное время задержки.
        Затем отправляет верное значение пароля в поле ввода пароля и нажимает кнопку отправки.
        Если появится поле ввода кода из смс, то тест проходит.
        В противном случае он завершается с информативным сообщением об ошибке.
        """
        self.input_login_field.send_keys(LOGIN)
        self.browser.find_element(By.ID, SUBMIT_BUTTON_ID).click()
        sleep(MAX_DELAY_SEC)
        input_password_field = self.browser.find_element(By.ID, PASSWORD_FIELD_ID)
        input_password_field.send_keys(PASSWORD)
        self.browser.find_element(By.ID, SUBMIT_BUTTON_ID).click()
        sleep(MAX_DELAY_SEC)
        phone_code_field = self.browser.find_element(By.ID, PHONE_CODE_ID)
        assert phone_code_field, f"Failed in test_true_password. Maybe password: {PASSWORD} - incorrect"
        sleep(MIN_DELAY_SEC)
