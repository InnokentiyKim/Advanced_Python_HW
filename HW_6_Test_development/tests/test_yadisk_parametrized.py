import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
url = "https://cloud-api.yandex.net/v1/disk/resources"
false_url = "https://cloud-api.yandex.net/v1/disk/esource"
params = {'path': 'Pictures_123'}
headers = {'Authorization': f"OAuth {TOKEN}"}
false_headers = {'Authorization': "OAuth"}


@pytest.mark.parametrize(
    'url,params,headers,status_code',
    [
        (url, params, headers, 201),
        (url, params, false_headers, 401),
        (false_url, params, headers, 404),
        (url, params, headers, 409),
    ]
)
def test_create_folder(url, params, headers, status_code):
    """
    Тестирование создания папки на Яндекс.Диске.
    Эта функция тестирует создание папки на Яндекс.Диске с помощью метода PUT.
    Она отправляет запрос на указанный `url` с указанными `params` и `headers` для аутентификации.
    Функция ожидает, что код состояния ответа будет соответствовать указанному `status_code`.
    Параметры:
        url (str): URL API Яндекс.Диска.
        params (dict): Параметры запроса API.
        headers (dict): Заголовки для аутентификации.
        status_code (int): Ожидаемый код состояния ответа.
    Выбрасывает AssertionError: Если код состояния ответа не соответствует ожидаемому `status_code`.
    """
    response = requests.put(url, params=params, headers=headers)
    assert response.status_code == status_code
