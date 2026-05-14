import allure
import jsonschema
import requests
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3" # Тут хранится базовый URL

class TestPet:
    @allure.feature("Pet")
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'

        with allure.step("Проверка текстового содержимого в ответе"):
            assert response.text == 'Pet deleted', "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            } # Передаём тело запроса
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 404, 'Код ответа не совпал с ожидаемым'

        with allure.step("Проверка текстового содержимого в ответе"):
            assert response.text == 'Pet not found', 'Текст ошибки не совпал с ожидаемым'

    @allure.title("Попытка получения информации о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 404, 'Код ответа не совпал с ожидаемым'

    @allure.title("Попытка добавления нового питомца")
    def test_create_new_pet(self):
        with allure.step("Отправка запроса на добавление нового питомца"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": ["string"],
                "tags": [
                    {
                        "id": 0,
                        "name": "string"
                    }
                ],
                "status": "available"
            }
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'
            jsonschema.validate(response.json(), PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
           assert response_json ['id'] == payload['id'], 'id питомца не совпадает с ожидаемым'
           assert response_json ['name'] == payload['name'], 'Имя питомца не совпадает с ожидаемым'
           assert response_json ['category'] == payload['category'], 'Категория питомца не совпадает с ожидаемой'
           assert response_json ['photoUrls'] == payload['photoUrls'], 'Фото питомца не совпадает с ожидаемым'
           assert response_json ['status'] == payload['status'], 'Статус питомца не совпадает с ожидаемым'

    @allure.title("Добавление нового питомца")
    def test_create_new_pet(self):
        with allure.step("Отправка запроса на добавление нового питомца"):
            payload = {
                    "id": 10,
                    "name": "Buddy",
                    "status": "available"
                   }
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'
            jsonschema.validate(response.json(), PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], 'id питомца не совпадает с ожидаемым'
            assert response_json['name'] == payload['name'], 'Имя питомца не совпадает с ожидаемым'
            assert response_json['status'] == payload['status'], 'Статус питомца не совпадает с ожидаемым'