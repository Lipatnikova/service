import allure
import pytest
import logging
from modules.entity import Entity
from generator.generator import generate_payload

logger = logging.getLogger("api")


class TestEntity:

    @allure.feature("Test-service")
    @allure.story("API")
    @allure.title("Получить данные сущности")
    @allure.description("""
    Цель: Посмотреть информацию о сущности и сравнить ее данные с ожидаемыми

    Шаги:
    1. Создать сущность
    2. Сравнить данные сущности с данными при создании сущности

    Постусловие: 
    - Удалить тестовые данные

    Ожидаемый результат: 
    - Сущность создана
    - Данные полученные в ответе соответствуют данным введенным при создании сущности
    """)
    @allure.testcase("TC_1")
    @pytest.mark.api
    def test_verify_get_entity(self, dell_entities):
        with allure.step("Создать сущность"):
            new_object = Entity()
            payload = generate_payload()
            id_entity = new_object.check_create_new_entity(payload)
            new_object.check_response_is_200()
            new_object.check_date_today()

        with allure.step("Сравнить данные сущности с данными при создании сущности"):
            response = new_object.check_get_entity_with_validate_response(id_entity)
            format_response = new_object.remove_keys(response, 'id')
            assert format_response == payload, \
                logger.warning("Данные полученные в ответе не соответствуют данным введенным при создании сущности")

    @allure.feature("Test-service")
    @allure.story("API")
    @allure.title("Получить список сущностей")
    @allure.description("""
    Цель: Посмотреть список сущностей

    Предусловие: Создано рандомное количество сущностей

    Шаги:
    1. Получить список сущностей 
    2. Проверить список сущностей

    Постусловие: 
    - Удалить тестовые данные

    Ожидаемый результат: 
    - Отображается список сущностей
    """)
    @allure.testcase("TC_2")
    @pytest.mark.api
    def test_verify_get_all_entities(self, create_random_entities, dell_entities):
        with allure.step("Получить список сущностей"):
            entities = Entity()
            entities.check_get_all_entities_with_validate_response()

        with allure.step("Проверить список сущностей"):
            entities.check_response_is_200()
            entities.check_count_headers()
            entities.check_content_type()

    @allure.feature("Test-service")
    @allure.story("API")
    @allure.title("Создание сущности")
    @allure.description("""
    Цель: Проверить создание сущности

    Шаги:
    1. Создать сущность
    2. Проверить создание сущности

    Постусловие: 
    - Удалить тестовые данные

    Ожидаемый результат: 
    - Сущность создана
    """)
    @allure.testcase("TC_3")
    @pytest.mark.api
    def test_verify_create_entity(self, dell_entities):
        with allure.step("Создать сущность"):
            new_object = Entity()
            data_new_entity = generate_payload()
            new_object.check_create_new_entity(data_new_entity)

        with allure.step("Проверить создание сущности"):
            new_object.check_response_is_200()
            new_object.check_count_headers()
            new_object.check_date_today()

    @allure.feature("Test-service")
    @allure.story("API")
    @allure.title("Обновление данных сущности")
    @allure.description("""
    Цель: Проверить обновление данных сущности

    Шаги:
    1. Создать сущность
    2. Обновить данные у сущности
    3. Проверить, что данные сущности изменились

    Постусловие: 
    - Удалить тестовые данные

    Ожидаемый результат: 
    - Данные сущности обновлены
    """)
    @allure.testcase("TC_4")
    @pytest.mark.api
    def test_create_and_update_entity(self):
        with allure.step("Создать сущность"):
            entity = Entity()
            data_new_entity = generate_payload()
            entity_id = entity.check_create_new_entity(data_new_entity)
            response_before = entity.check_get_entity_with_validate_response(entity_id)
            new_payload = entity.modify_payload(response_before)

        with allure.step("Обновить данные у сущности"):
            entity.update_entity_with_validate_response(id, new_payload)
            entity.check_response_is_204()
            entity.check_date_today()
            response_after = entity.check_get_entity_with_validate_response(id)
            response_after = entity.remove_keys(response_after, 'id')

        with allure.step("Проверить, что данные сущности изменились"):
            assert data_new_entity != response_after, \
                logger.warning('Entity data has not been updated, matches the data when the entity was created')

            entity.delete_entity(id)

    @allure.feature("Test-service")
    @allure.story("API")
    @allure.title("Удалить из списока сущностей рандомную сущность")
    @allure.description("""
     Цель: Проверить удаление сущности

    Предусловие: Создано рандомное количество сущностей

    Шаги:
    1. Получить список сущностей
    2. Удалить рандомную сущность из списка
    3. Проверить, что в списке сущностей отсутствует удаленная сущность

    Постусловие: 
    - Удалить тестовые данные

    Ожидаемый результат: 
    - Отображается список сущностей без удаленной сущности
    """)
    @allure.testcase("TC_5")
    @pytest.mark.api
    def test_check_delete_random_entity_by_random_id(self, create_random_entities):
        pass
