import os
import requests
from dotenv import load_dotenv

load_dotenv()


class TestYandexDisk:
    def setup_method(self):
        self.TOKEN = os.getenv("TOKEN")
        self.url = "https://cloud-api.yandex.net/v1/disk/resources"
        self.false_url = "https://cloud-api.yandex.net/v1/disk/esource"
        self.params = {'path': 'Pictures_123'}
        self.headers = {'Authorization': f"OAuth {self.TOKEN}"}
        self.false_headers = {'Authorization': "OAuth"}

    def teardown_method(self):
        requests.delete(self.url, params=self.params, headers=self.headers)

    def test_create_folder_201(self):
        response = requests.put(self.url, params=self.params, headers=self.headers)
        assert response.status_code == 201

    def test_create_folder_401(self):
        response = requests.put(self.url, params=self.params, headers=self.false_headers)
        assert response.status_code == 401

    def test_create_folder_404(self):
        response = requests.put(self.false_url, params=self.params, headers=self.headers)
        assert response.status_code == 404

    def test_create_folder_409(self):
        requests.put(self.url, params=self.params, headers=self.headers)
        second_response = requests.put(self.url, params=self.params, headers=self.headers)
        assert second_response.status_code == 409
