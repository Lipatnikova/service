import logging
import random
import requests
import string
from datetime import datetime
from typing import Dict, Any, List, Union
from utils.http_handler import HTTPHandler
from data.endpoints import UrlAndEndPoints as EndPoint
from data.expected_result import StatusCode, Expected

logger = logging.getLogger("api")


class Entity:
    def __init__(self):
        self.response = None
        self.response_json = None

    def check_create_new_entity(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Method to check scheme json and create a new entity using the provided payload"""
        self.response = HTTPHandler.post(EndPoint.CREATE_ENTITY, payload)
        self.response_json = self.response.json()
        return self.response_json

    def delete_entity(self, entity_id: str) -> Dict[str, Any]:
        """The method to delete an entity by its ID"""
        self.response = HTTPHandler.delete(f'{EndPoint.DEL_ENTITY}{entity_id}')
        return self.response_json

    def check_get_entity_with_validate_response(self, entity_id: dict[str, Any]) -> Dict[str, Any]:
        """The method to retrieve an entity by its ID and validate the response"""
        self.response = HTTPHandler.get(f'{EndPoint.ENTITY}{entity_id}')
        self.response_json = self.response.json()
        return self.response_json

    def extract_ids(self, response_json: Dict[str, Any]) -> List[str]:
        """The method to extract IDs from the response"""
        return [item['id'] for item in response_json['entity']]

    def check_get_all_entities_with_validate_response(self) -> List[str]:
        """The method to retrieve all entities and validate the response"""
        self.response = HTTPHandler.get(EndPoint.ENTITIES, schemas='all_entities.json')
        self.response_json = self.response.json()
        return self.extract_ids(self.response_json)

    def get_random_id(self, list_ids: List[str]) -> str:
        """The method to retrieve a random ID from the provided list of IDs"""
        return random.choice(list_ids)

    def update_entity(self, entity_id: dict[str, Any], payload: Dict[str, Any]) -> requests.Response:
        """The method to update an entity by its ID with the provided payload"""
        self.response = HTTPHandler.patch(f'{EndPoint.CHANGE_ENTITY}{entity_id}', data=payload)
        return self.response

    def check_response_is_200(self) -> None:
        """The method to check if the response status code is 200 (OK)"""
        status_code = self.response.status_code
        assert status_code == StatusCode.OK, \
            logger.warning(
                f'Response status code is incorrect, actual: {status_code}, expected : {StatusCode.OK}'
            )

    def check_response_is_204(self) -> None:
        """The method to check if the response status code is 204 (No Content)"""
        status_code = self.response.status_code
        assert status_code == StatusCode.NO_CONTENT, \
            logger.warning(
                f'Response status code is incorrect, actual: {status_code}, expected : {StatusCode.NO_CONTENT}'
            )

    def check_response_is_500(self) -> None:
        """The method to check if the response status code is 500 (Internal Server Error)"""
        status_code = self.response.status_code
        assert status_code == StatusCode.INTERNAL_ERROR, \
            logger.warning(
                f'Response status code is incorrect, actual: {status_code}, expected : {StatusCode.INTERNAL_ERROR}'
            )

    def check_count_headers(self) -> None:
        """The method to check if the count of headers in the response is correct"""
        count_headers = len(self.response.headers)
        assert count_headers == Expected.count_headers, logger.warning(
            f'Count of headers is not correct, actual: {count_headers}, expected : {Expected.count_headers}'
        )

    def check_content_type(self) -> None:
        """The method to check if the Content-Type header in the response is correct"""
        content_type = self.response.headers['Content-Type']
        assert Expected.content_type in content_type, \
            logger.warning('The headers Content-Type is wrong')

    def check_date_today(self) -> None:
        """The method to check if the Date header in the response matches the current date"""
        date_response = self.response.headers['Date'][5:16]
        change_format_date_response = datetime.strptime(date_response, "%d %b %Y")
        change_format_date_response = change_format_date_response.strftime("%Y-%m-%d")
        today = str(datetime.today())[:10]
        assert today == change_format_date_response, \
            logger.warning('The entity creation date does not match the current day')

    def remove_keys(self, d: Union[Dict[str, Any], List[Any]], key: Any) -> Union[Dict[str, Any], List[Any]]:
        """The method to remove keys from a dictionary or a list of dictionaries recursively"""
        if isinstance(d, dict):
            return {k: self.remove_keys(v, key) for k, v in d.items() if k != key}
        elif isinstance(d, list):
            return [self.remove_keys(v, key) for v in d]
        else:
            return d

    def modify_payload(self, new_payload: Dict[str, Any]) -> Dict[str, Any]:
        """The method to modify a payload by removing specified keys and adding additional information"""
        keys_to_remove = ['id', 'verified']
        new_payload = {key: value for key, value in new_payload.items() if key not in keys_to_remove}
        new_payload['addition']['additional_info'] = ''.join(random.choices(string.ascii_letters, k=10))
        return new_payload
