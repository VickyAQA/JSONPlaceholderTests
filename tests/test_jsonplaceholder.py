import allure
import requests
import pytest
from pydantic import BaseModel, ValidationError
from core.models.comment import Comment
from typing import List


@allure.feature("API постов")
@allure.story("Позитивный: Получение всех постов")
def test_get_all_publications(api_client):
    with allure.step("Отправка GET запроса к /posts"):
        publications = api_client.get_all_publications()
    with allure.step("Проверка, что ответ - это список"):
        assert isinstance(publications, list), "Ожидаем список постов"

@allure.feature("API постов")
@allure.story("Позитивный: Получение получение информации о посте по ID")
def test_get_publication_by_id(api_client, create_publication):
    publication_id = create_publication["id"]

    with allure.step(f"Получение поста с ID"):
        publication = api_client.get_publication_by_id(publication_id)

    with allure.step("Проверка, что получен правильный пост"):
        assert publication["id"] == publication_id, f"Expected post ID {publication_id}, but got {publication['id']}"

@allure.feature("API постов")
@allure.story("Негативный: Получение поста с невалидным ID")
def test_get_publication_with_invalid_id(api_client):
    invalid_publication_id = "invalid_id"
    with allure.step(f"Ожидание ошибки при получении поста с невалидным ID: {invalid_publication_id}"):
        with pytest.raises(AssertionError) as excinfo:
            api_client.get_publication_by_id(invalid_publication_id)

@allure.feature("API постов")
@allure.story("Позитивный: Получение поста с комментарием")
def test_get_posts_comments(api_client):
    with allure.step("Получение комментариев к посту 1"):
        response = api_client.get_publications_comments(post_id=1)
        response.raise_for_status()
        data = response.json()
        try:
            comments: List[Comment] = [Comment(**item) for item in data]
        except ValidationError as e:
            pytest.fail(f"Ошибка валидации Pydantic: {e}")
            assert len(comments) > 0, "Список комментариев пуст"
            for comment in comments:
                assert comment.postId == 1, "postId должен быть 1"




