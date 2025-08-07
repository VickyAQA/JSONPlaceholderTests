import  requests
import os
from  dotenv import load_dotenv
from core.settings.enviroments import Environment
import allure
from core.clients.endpoints import Endpoints
load_dotenv()


class APIClient:
    def __init__(self):
        environment_str = os.getenv('ENVIRONMENT', 'TEST')
        try:
            self.environment = Environment[environment_str]
        except KeyError:
            raise ValueError(f"Unsupported environment value: {environment_str}")

        self.base_url = self.get_base_url(self.environment)
        self.session = requests.Session()

    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv('TEST_BASE_URL')
        elif environment == Environment.PROD:
            return os.getenv('PROD_BASE_URL')
        else:
            raise ValueError(f"Unsupported environment: {environment}")

    def get_all_publications(self):
        with allure.step("Получение всех постов"):
            url = f"{self.base_url}{Endpoints.POSTS_ENDPOINT.value}"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()

    def get_publication_by_id(self, posts_id):
        with allure.step("Получение поста по ID"):
            url = f"{self.base_url}{Endpoints.POSTS_ENDPOINT.value}/{posts_id}"
            response = self.session.get(url)
            assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
            return response.json()

    def get_publications_comments(self, status_code=200, post_id=1):
        with allure.step("Получение комментариев к постам"):
            url = f"{self.base_url}/posts/{post_id}/comments"
            response = self.session.get(url)
            assert response.status_code == status_code, f"Unexpected status code: {response.status_code}"
            return response


