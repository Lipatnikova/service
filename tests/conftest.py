import pytest
import random
from generator.generator import generate_payload
from modules.entity import Entity


@pytest.fixture()
def dell_entities():
    yield
    entities = Entity()
    ids = entities.check_get_all_entities_with_validate_response()
    for i in ids:
        entities.delete_entity(i)
        entities.check_response_is_204()
        entities.delete_entity(i)
        entities.check_response_is_500()


@pytest.fixture()
def create_random_entities():
    """Create a random number of entities using the check_create_new_entity method"""
    entities = []
    new_object = Entity()
    for _ in range(random.randint(2, 10)):
        payload = generate_payload()
        entity_json = new_object.create_new_entity(payload)
        entities.append(entity_json)
    return len(entities)
