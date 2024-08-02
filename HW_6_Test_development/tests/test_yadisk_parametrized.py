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
    response = requests.put(url, params=params, headers=headers)
    assert response.status_code == status_code
