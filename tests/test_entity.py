import allure
import pytest
from modules.entity import SendRequest, Assertions, ConversionData
from generator.generator import generate_payload, modify_payload


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
            new_object = SendRequest()
            payload = generate_payload()
            response = new_object.create_new_entity(payload)
            id_entity = ConversionData.get_id_created_entity(response)
            Assertions.check_date_today(response)

        with allure.step("Сравнить данные сущности с данными при создании сущности"):
            response = new_object.check_get_entity_with_validate_response(id_entity)
            format_response = ConversionData.remove_keys(response, 'id')
            assert format_response == payload, \
                "Data received in the response does not match the data entered when creating the entity"

    @allure.feature("Test-service")
    @allure.story("API")
    @allure.title("Получить список сущностей")
    @allure.description("""
    Цель: Посмотреть список сущностей

    Предусловие: Создано рандомное количество сущностей

    Шаги:
    1. Получить список сущностей 
    2. Проверить список сущностей, количество сущностей полученных должно 
    соответствовать колучеству создаваемых сущностей

    Постусловие: 
    - Удалить тестовые данные

    Ожидаемый результат: 
    - Отображается список сущностей
    """)
    @allure.testcase("TC_2")
    @pytest.mark.api
    def test_verify_get_all_entities(self, create_random_entities, dell_entities):
        expected_count_entities = create_random_entities
        with allure.step("Получить список сущностей"):
            entities = SendRequest()
            response_json = entities.check_get_all_entities_with_validate_response_json()
            ids = ConversionData.extract_ids(response_json)
            actual_count_ids = ConversionData.get_count_entities(ids)
        with allure.step("Проверить список сущностей, количество сущностей полученных должно "
                         "соответствовать колучеству создаваемых сущностей"):
            assert expected_count_entities == actual_count_ids, \
                "The count of entities received does not match the count of entities created"

    @allure.feature("Test-service")
    @allure.story("API")
    @allure.title("Создание сущности")
    @allure.description("""
    Цель: Проверить создание сущности

    Шаги:
    1. Создать сущность
    2. Проверить, что в списке всех сущностей имеется запись 
    с additional_info сгенерированной при создании сущности"

    Постусловие: 
    - Удалить тестовые данные

    Ожидаемый результат: 
    - Сущность создана
    """)
    @allure.testcase("TC_3")
    @pytest.mark.api
    def test_verify_create_entity(self, dell_entities):
        with allure.step("Создать сущность"):
            new_object = SendRequest()
            data_new_entity = generate_payload()
            response = new_object.create_new_entity(data_new_entity)

        with allure.step("Проверить, что в списке всех сущностей имеется запись "
                         "с additional_info сгенерированной при создании сущности"):
            Assertions.check_date_today(response)
            all_entities = new_object.check_get_all_entities_with_validate_response_json()
            expected_additional_info = ConversionData.extract_additional_info(data_new_entity)
            actual_additional_info = ConversionData.extract_additional_info_all_entity(all_entities)
            assert expected_additional_info == actual_additional_info, \
                "List all entities does not contain an entry with expected 'additional_info'"

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
    def test_create_and_update_entity(self, dell_entities):
        with allure.step("Создать сущность"):
            entity = SendRequest()
            data_new_entity = generate_payload()
            response = entity.create_new_entity(data_new_entity)
            entity_id = ConversionData.get_id_created_entity(response)
            response_before = entity.check_get_entity_with_validate_response(entity_id)
            new_payload = modify_payload(response_before)

        with allure.step("Обновить данные у сущности"):
            response = entity.update_entity(entity_id, new_payload)
            Assertions.check_response_is_204(response)
            Assertions.check_date_today(response)
            response_after = entity.check_get_entity_with_validate_response(entity_id)
            response_after = ConversionData.remove_keys(response_after, "id")

        with allure.step("Проверить, что данные сущности изменились"):
            assert data_new_entity != response_after, \
                "Entity data has not been updated, matches the data when the entity was created"

    @allure.feature("Test-service")
    @allure.story("API")
    @allure.title("Удалить из списка сущностей рандомную сущность")
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
    def test_check_delete_random_entity_by_random_id(self, create_random_entities, dell_entities):
        with allure.step("Получить список сущностей"):
            entities = SendRequest()
            response_json = entities.check_get_all_entities_with_validate_response_json()
            ids = ConversionData.extract_ids(response_json)

        with allure.step("Удалить рандомную сущность"):
            random_id_entity = ConversionData.get_random_id(ids)
            response = entities.delete_entity(random_id_entity)
            Assertions.check_response_is_204(response)
            response = entities.delete_entity(random_id_entity)
            Assertions.check_response_is_500(response)

        with allure.step("Проверить, что в списке сущностей отсутствует удаленная сущность"):
            response = entities.check_get_all_entities_with_validate_response_json()
            list_entity = ConversionData.extract_ids(response)
            assert (random_id_entity in list_entity) is False, \
                'The entity with the selected ID was not deleted'
