import allure
import requests
import pytest
from conftest import api_client, create_payload
from pydantic import ValidationError
from core.models.comment import Comment


@allure.feature("API постов")
@allure.story("Позитивный: Получение всех постов")
def test_get_all_posts(api_client):
    with allure.step("Отправка GET запроса к /posts"):
        posts = api_client.get_all_posts()
    with allure.step("Проверка, что ответ - это список"):
        assert isinstance(posts, list), "Ожидаем список постов"
    with allure.step("Получаем список из 100 постов"):
        assert len(posts) == 100

@allure.feature("API постов")
@allure.story("Позитивный: Получение получение информации о посте по ID")
def test_get_posts_by_id(api_client, create_payload):
    post_id = create_payload["id"]

    with allure.step(f"Получение поста с ID"):
        post = api_client.get_posts_by_id(post_id)

    with allure.step("Проверка, что получен правильный пост"):
        assert post["id"] == post_id, f"Expected post ID {post_id}, but got {post['id']}"

@allure.feature("API постов")
@allure.story("Негативный: Получение поста с невалидным ID")
def test_get_post_with_invalid_id(api_client):
    invalid_post_id = "invalid_id"
    with allure.step(f"Ожидание ошибки при получении поста с невалидным ID: {invalid_post_id}"):
        with pytest.raises(requests.exceptions.HTTPError) as excinfo:
            api_client.get_posts_by_id(invalid_post_id)

@allure.feature("API постов")
@allure.story("Позитивный: Получение поста с комментарием")
def test_get_posts_comments(api_client):
    with allure.step("Отправка GET запроса к /posts"):
        response = api_client.get_posts_comments(post_id=1)
        data = response.json()
        if data:
            for item in data:
                try:
                    Comment(**item)
                except ValidationError as e:
                    raise ValidationError(f"Response validation failed: {e}")








