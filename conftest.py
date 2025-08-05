import pytest
import requests
from core.clients.api_client import APIClient
import random

@pytest.fixture(scope="session")
def api_client():
    client = APIClient()
    return  client


@pytest.fixture()
def create_payload():
    """Фикстура для создания ответа."""

    payload = {
        "userId": 1,
        "id": 1,
        "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
        "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
    }
    return payload

@pytest.fixture
def random_post_id():
    """Фикстура, возвращающая случайный ID поста (от 1 до 100)."""
    return random.randint(1, 100)