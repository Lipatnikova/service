import pytest
import random
from generator.generator import generate_payload
from modules.entity import Entity


@pytest.fixture()
def dell_entities():
    def dell_all_entities():
        entities = Entity()
        ids = entities.check_get_all_entities_with_validate_response()
        for i in ids:
            entities.delete_entity(i)
            entities.check_response_is_204()
            entities.delete_entity(i)
            entities.check_response_is_500()

    yield dell_all_entities()


@pytest.fixture()
def create_random_entities():
    entities = Entity()
    for _ in range(random.randint(2, 10)):
        entities.check_create_new_entity(generate_payload())
