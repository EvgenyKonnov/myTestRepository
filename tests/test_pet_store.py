import allure
import jsonschema
import requests
from .schemas.store_schema import STORE_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

class TestPetStore:
    @allure.feature("Store")
    @allure.title("Размещение заказа")
    def test_create_new_order(self, create_order):
        with allure.step("Отправка запроса на размещение заказа"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=create_order)
            response_json = response.json()

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'
            jsonschema.validate(response.json(), STORE_SCHEMA)

        with (allure.step("Проверка параметров заказа в ответе")):
            assert response_json['id'] == create_order["id"], 'ID заказа не совпадает с ожидаемым'
            assert response_json['petId'] == create_order['petId'], 'ID питомца в заказе не совпадает с ожидаемым'
            assert response_json['quantity'] == create_order['quantity'], 'Количество товара в заказе не совпадает с ожидаемым'
            assert response_json['status'] == create_order['status'], 'Статус заказа не совпадает с ожидаемым'
            assert response_json['complete'] == create_order['complete'], 'Выполнение заказа не совпадает с ожидаемым'

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order['id']

        with allure.step("Получение информации о заказе по ID"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")
            response_json = response.json()

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'

        with allure.step("Проверка параметров заказа в ответе"):
            assert response_json['id'] == create_order["id"], 'ID заказа не совпадает с ожидаемым'
            assert response_json['petId'] == create_order['petId'], 'ID питомца в заказе не совпадает с ожидаемым'
            assert response_json['quantity'] == create_order['quantity'], 'Количество товара в заказе не совпадает с ожидаемым'
            assert response_json['status'] == create_order['status'], 'Статус заказа не совпадает с ожидаемым'
            assert response_json['complete'] == create_order['complete'], 'Выполнение заказа не совпадает с ожидаемым'

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order['id']

        with allure.step("Отправка запроса на удаление заказа по ID"):
            response = requests.delete(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'

        with allure.step("Получение информации о заказе по ID"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 404, 'Код ответа не совпал с ожидаемым'

    @allure.title("Получение информации о заказе по несуществующему ID")
    def test_get_order_by_nonexistent_id(self):
        with allure.step("Получение информации о заказе по несуществующему ID"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 404, 'Код ответа не совпал с ожидаемым'

    @allure.title("Получение инвентаря магазина")
    def test_get_order_inventory(self):
        with allure.step("Получение инвентаря магазина"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")
            response_json = response.json()

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'

        with allure.step("Проверка текстового содержимого в ответе"):
            assert response.text == '{"approved":135,"placed":6,"delivered":26}', "Текст ошибки не совпал с ожидаемым"



