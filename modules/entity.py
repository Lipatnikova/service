import logging
import random
from typing import Dict, Any, Union
from datetime import datetime
from data.endpoints import UrlAndEndPoints as EndPoint
from data.expected_result import StatusCode
from utils.http_handler import HTTPHandler
from utils.models.pydantic_models import *


logger = logging.getLogger("api")


class Entity:
    def __init__(self):
        self.response = None
        self.response_json = None

    def create_new_entity(self, payload: Dict):
        """Method to check scheme json and create a new entity using the provided payload"""
        self.response = HTTPHandler.post(payload)
        return self.response

    def get_id_created_entity(self):
        """Retrieves the ID of the created entity from the response JSON"""
        self.response_json = self.response.json()
        return self.response_json

    def delete_entity(self, entity_id: str):
        """The method to delete an entity by its ID"""
        self.response = HTTPHandler.delete(f'{EndPoint.DEL_ENTITY}{entity_id}')
        return self.response

    def check_get_entity_with_validate_response(self, entity_id: int):
        """The method to retrieve an entity by its ID and validate the response"""
        self.response_json = HTTPHandler.get_with_validation(f'{EndPoint.ENTITY}{entity_id}', EntityModel)
        return self.response_json

    def check_get_all_entities_with_validate_response_json(self) -> List[str]:
        """The method to retrieve all entities and validate the response"""
        self.response_json = HTTPHandler.get_with_validation(EndPoint.ENTITIES, EntitiesModel)
        return self.response_json

    def update_entity(self, entity_id, payload: Dict):
        """The method to update an entity by its ID with the provided payload"""
        self.response = HTTPHandler.patch(f'{EndPoint.CHANGE_ENTITY}{entity_id}', payload)
        return self.response

    def extract_additional_info(self, data_new_entity):
        """Extracts the additional info from the provided new entity data"""
        return data_new_entity.get('addition', {}).get('additional_info')

    def extract_additional_info_all_entity(self, all_entities):
        """Extracts the additional info from the provided all entities data"""
        entity = all_entities.get('entity', [])[0]
        return entity.get('addition', {}).get('additional_info')

    def extract_ids(self, response_json: Dict[str, Any]) -> List[str]:
        """The method to extract IDs from the response"""
        return [item['id'] for item in response_json['entity']]

    def check_get_all_entities_with_validate_response(self) -> List[str]:
        """The method to retrieve all entities and validate the response"""
        self.response_json = HTTPHandler.get_with_validation(EndPoint.ENTITIES, EntitiesModel)
        return self.extract_ids(self.response_json)

    def get_count_entities(self) -> int:
        """The method counts IDs entities"""
        self.response_json = HTTPHandler.get_with_validation(EndPoint.ENTITIES, EntitiesModel)
        return len(self.extract_ids(self.response_json))

    def get_random_id(self, list_ids: List[str]) -> str:
        """The method to retrieve a random ID from the provided list of IDs"""
        return random.choice(list_ids)

    def remove_keys(self, d: Union[Dict[str, Any], List[Any]], key: Any) -> Union[Dict[str, Any], List[Any]]:
        """The method to remove keys from a dictionary or a list of dictionaries recursively"""
        if isinstance(d, dict):
            return {k: self.remove_keys(v, key) for k, v in d.items() if k != key}
        elif isinstance(d, list):
            return [self.remove_keys(v, key) for v in d]
        else:
            return d


class Assertions:

    @staticmethod
    def check_response_is_204(response) -> None:
        """The method to check if the response status code is 204 (No Content)"""
        status_code = response.status_code
        assert status_code == StatusCode.NO_CONTENT, \
            logger.warning(
                f'Response status code is incorrect, actual: {status_code}, expected : {StatusCode.NO_CONTENT}'
            )

    @staticmethod
    def check_response_is_500(response) -> None:
        """The method to check if the response status code is 500 (Internal Server Error)"""
        status_code = response.status_code
        assert status_code == StatusCode.INTERNAL_ERROR, \
            logger.warning(
                f'Response status code is incorrect, actual: {status_code}, expected : {StatusCode.INTERNAL_ERROR}'
            )

    @staticmethod
    def check_date_today(response) -> None:
        """The method to check if the Date header in the response matches the current date"""
        date_response = response.headers['Date'][5:16]
        change_format_date_response = datetime.strptime(date_response, "%d %b %Y")
        change_format_date_response = change_format_date_response.strftime("%Y-%m-%d")
        today = str(datetime.today())[:10]
        assert today == change_format_date_response, \
            logger.warning('The entity creation date does not match the current day')
