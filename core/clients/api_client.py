import requests
import os
from dotenv import load_dotenv
from urllib3.contrib.emscripten import response
from core.settings.environments import Environment
from core.settings.config import Users, Timeouts
import allure
from core.clients.endpoints import Endpoints
from tests.schemas.booking_schema import BOOKING_SCHEMA
from tests.conftest import create_booking

load_dotenv()

class APIClient:
    def __init__(self):
        environment_str = os.getenv("ENVIRONMENT")
        try:
            environment = Environment(environment_str)
        except KeyError:
            raise ValueError(f"Unsupported environment value {environment_str}")

        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()
        self.session.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv('TEST_BASE_URL')
        elif environment == Environment.PROD:
            return os.getenv('PROD_BASE_URL')
        else:
            raise ValueError(f"Unsupported environment: {environment}")

    def ping(self):
        with allure.step('Ping api client'):
            url = f"{self.base_url}{Endpoints.PING_ENDPOINT}" # Формируем переменную URL адреса
            response = self.session.get(url)                  # Обращаемся к сессии и подставляем URL адрес
            response.raise_for_status()                       # Проверям отсутствие HTTP ошибок
        with allure.step('Assert status code'):
            assert response.status_code == 201, f'Expected status code of 201, but got {response.status_code}' # Проверям статус код
        return response.status_code # Возвращаем статус код

    def auth(self):
        with allure.step('Getting authenticate'):
            url = f"{self.base_url}{Endpoints.AUTH_ENDPOINT}" # Формируем переменную URL адреса
            payload = {"username": Users.USERNAME, "password": Users.PASSWORD} # Передаём тело
            response = self.session.post(url, json=payload, timeout = Timeouts.TIMEOUT) # Выполняем POST запрос и передаём тело и Timeout
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f'Expected status code of 201, but got {response.status_code}'
        token = response.json().get('token')
        with allure.step('Updating headers with autorization'):
            self.session.headers.update({'Authorization': f'Bearer {token}'})  # Обновляем заголовки (добавляем Token)

    def get_booking_by_id(self, create_booking):
        with allure.step('Getting booking by id'):
            booking_id = create_booking['bookingid']
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}{booking_id}"  # Формируем переменную URL адреса
            response = self.session.get(url, timeout = Timeouts.TIMEOUT)
            response_json = response.json()
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f'Expected status code of 201, but got {response.status_code}'
        with allure.step("Checking booking fields"):
            assert response_json['bookingid'] == create_booking["bookingid"], 'Параметр bookingid не совпадает с ожидаемым'
            assert response_json['firstname'] == create_booking['firstname'], 'Параметр firstname не совпадает с ожидаемым'
            assert response_json['lastname'] == create_booking['lastname'], 'Параметр lastname не совпадает с ожидаемым'
            assert response_json['totalprice'] == create_booking['totalprice'], 'Параметр totalprice не совпадает с ожидаемым'
            assert response_json['depositpaid'] == create_booking['depositpaid'], 'Параметр depositpaid не совпадает с ожидаемым'
            assert response_json['bookingdates'] == create_booking['bookingdates'], 'Параметр bookingdates не совпадает с ожидаемым'
            assert response_json['additionalneeds'] == create_booking['additionalneeds'], 'Параметр additionalneeds не совпадает с ожидаемым'
