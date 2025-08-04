import  requests
import os
from  dotenv import load_dotenv
from core.settings.enviroments import Environment
import allure
load_dotenv()
from core.clients.endpoints import Endpoints

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

    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = self.session.get(url, headers=self.session.headers, params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def get_all_posts(self):
        with allure.step("Получение всех постов"):
            return self.get(Endpoints.POSTS_ENDPOINT.value)

    def post(self, endpoint, data=None, status_code=200):
        url = self.base_url + endpoint
        response = self.session.post(url, headers=self.session.headers, json=data)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def get_posts_by_id(self, posts_id):
        with allure.step("Return posts by id"):
            url = f"{self.base_url}{Endpoints.POSTS_ENDPOINT.value}/{posts_id}"
            response = self.session.get(url, headers=self.session.headers)
            if response.status_code == 404:
                raise requests.exceptions.HTTPError(f"Post not found (status code: 404)", response=response)
            elif response.status_code != 200:
                raise requests.exceptions.HTTPError(f"Unexpected status code: {response.status_code}", response=response)
            response.raise_for_status()
            return response.json()

    def get_posts_comments(self, status_code=200):
        with allure.step("Return posts by id"):
            url = f"{self.base_url}{Endpoints.POST_COMMENTS_ENDPOINT.value}"
            response = self.session.get(url, headers=self.session.headers)
            if status_code:
                assert response.status_code == status_code
            return response.json()

