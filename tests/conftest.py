import pytest
import random
from generator.generator import generate_payload
from modules.entity import SendRequest, Assertions, ConversionData


@pytest.fixture()
def dell_entities():
    yield
    entities = SendRequest()
    response_json = entities.check_get_all_entities_with_validate_response_json()
    ids = ConversionData.extract_ids(response_json)
    for i in ids:
        response = entities.delete_entity(i)
        Assertions.check_response_is_204(response)
        response = entities.delete_entity(i)
        Assertions.check_response_is_500(response)


@pytest.fixture()
def create_random_entities():
    """Create a random number of entities using the check_create_new_entity method"""
    entities = []
    new_object = SendRequest()
    for _ in range(random.randint(2, 10)):
        payload = generate_payload()
        entity_json = new_object.create_new_entity(payload)
        entities.append(entity_json)
    return len(entities)
