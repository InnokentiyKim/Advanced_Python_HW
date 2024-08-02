import os
import requests
from dotenv import load_dotenv

load_dotenv()


class TestYandexDisk:
    def setup_method(self):
        """
        Setup метод. Настройка тестового окружения перед каждым тестовым случаем. Инициализирует необходимые
        переменные для тестовых случаев: токен Яндекс Диска `TOKEN`, `url` ссылка на API Яндекс.Диска,
        `false_url` несуществующая ссылка, параметры `params` запроса к API, заголовки авторизации `headers`,
        некорректный заголовок авторизации `false_headers`.
        """
        self.TOKEN = os.getenv("TOKEN")
        self.url = "https://cloud-api.yandex.net/v1/disk/resources"
        self.false_url = "https://cloud-api.yandex.net/v1/disk/esource"
        self.params = {'path': 'Pictures_123'}
        self.headers = {'Authorization': f"OAuth {self.TOKEN}"}
        self.false_headers = {'Authorization': "OAuth"}

    def teardown_method(self):
        """
        Teardown метод. Удаление ресурса (папки) с Яндекс Диска.
        Используется для очистки ресурсов, созданных во время тестирования.
        Вызывается после каждого тестового случая.
        """
        requests.delete(self.url, params=self.params, headers=self.headers)

    def test_create_folder_201(self):
        """
        Тестирование положительного сценария создания папки на Яндекс.Диск. Эта функция отправляет
        запрос PUT на API Яндекс.Диска для создания папки с указанным путем в параметре `params`.
        Запрос авторизуется с использованием параметра `headers`, содержащего токен авторизации.
        Функция ожидает, что код состояния ответа будет равен 201, указывая на успешное создание папки.
        Если код состояния не равен 201, тест не будет пройден.
        """
        response = requests.put(self.url, params=self.params, headers=self.headers)
        assert response.status_code == 201

    def test_create_folder_401(self):
        """
        Тестирование отрицательного сценария создания папки на Яндекс.Диск. Эта функция отправляет
        запрос PUT на API Яндекс.Диска для создания папки с указанным путем в параметре `params`.
        Запрос авторизуется с использованием параметра `headers`, содержащего токен авторизации.
        Функция ожидает, что код состояния ответа будет равен 401, указывая на отсутствие авторизации.
        Если код состояния не равен 401, тест не будет пройден.
        """
        response = requests.put(self.url, params=self.params, headers=self.false_headers)
        assert response.status_code == 401

    def test_create_folder_404(self):
        """
        Тестирование отрицательного сценария создания папки на Яндекс.Диск. Эта функция отправляет
        запрос PUT на API Яндекс.Диска для создания папки с указанным путем в параметре `params`.
        Запрос авторизуется с использованием параметра `headers`, содержащего токен авторизации.
        Функция ожидает, что код состояния ответа будет равен 404, указывая на отсутствие ресурса.
        Если код состояния не равен 404, тест не будет пройден.
        """
        response = requests.put(self.false_url, params=self.params, headers=self.headers)
        assert response.status_code == 404

    def test_create_folder_409(self):
        """
        Тестирование отрицательного сценария создания папки на Яндекс.Диск. Эта функция отправляет
        запрос PUT на API Яндекс.Диска для создания папки с указанным путем в параметре `params`.
        Запрос авторизуется с использованием параметра `headers`, содержащего токен авторизации.
        Функция ожидает, что код состояния ответа будет равен 409, указывая на то, что ресурс уже существует.
        Если код состояния не равен 409, тест не будет пройден.
        """
        requests.put(self.url, params=self.params, headers=self.headers)
        second_response = requests.put(self.url, params=self.params, headers=self.headers)
        assert second_response.status_code == 409
