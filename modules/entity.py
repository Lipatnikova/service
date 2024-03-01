import random
import string
from datetime import datetime

from generator.generator import generate_payload
from utils.http_handler import HTTPHandler
from data.endpoints import UrlAndEndPoints as EndPoint
import logging
from data.expected_result import StatusCode, ExpectedText

logger = logging.getLogger("api")


class Entity:
    def __init__(self):
        self.response = None
        self.response_json = None

    def check_create_new_entity(self, payload):
        self.response = HTTPHandler.post(EndPoint.CREATE_ENTITY, payload)
        self.response_json = self.response.json()
        return self.response_json

    def create_random_entities(self):
        count = random.randint(1, 10)
        for _ in range(count):
            self.check_create_new_entity(generate_payload())
        return count

    def delete_entity(self, entity_id):
        self.response = HTTPHandler.delete(f'{EndPoint.DEL_ENTITY}{entity_id}')
        return self.response_json

    def check_get_entity_with_validate_response(self, entity_id):
        self.response = HTTPHandler.get(f'{EndPoint.ENTITY}{entity_id}')
        self.response_json = self.response.json()
        return self.response_json

    def extract_ids(self, response_json):
        return [item['id'] for item in response_json['entity']]

    def check_get_all_entities_with_validate_response(self):
        self.response = HTTPHandler.get(EndPoint.ENTITIES, schemas='all_entities.json')
        self.response_json = self.response.json()
        return self.extract_ids(self.response_json)

    def get_random_id(self, list_ids):
        return random.choice(list_ids)

    def update_entity_with_validate_response(self, entity_id, payload):
        self.response = HTTPHandler.patch(f'{EndPoint.CHANGE_ENTITY}{entity_id}', data=payload)
        return self.response

    def check_response_is_200(self):
        status_code = self.response.status_code
        assert status_code == StatusCode.OK, \
            logger.warning(
                f'Response status code is incorrect, actual: {status_code}, expected : {StatusCode.OK}'
            )

    def check_response_is_204(self):
        status_code = self.response.status_code
        assert status_code == StatusCode.NO_CONTENT, \
            logger.warning(
                f'Response status code is incorrect, actual: {status_code}, expected : {StatusCode.NO_CONTENT}'
            )

    def check_response_is_500(self):
        status_code = self.response.status_code
        assert status_code == StatusCode.INTERNAL_ERROR, \
            logger.warning(
                f'Response status code is incorrect, actual: {status_code}, expected : {StatusCode.INTERNAL_ERROR}'
            )

    def check_count_headers(self):
        count_headers = len(self.response.headers)
        assert count_headers == 3, logger.warning(
            f'Count of headers is not correct, actual: {count_headers}, expected : 3'
        )

    def check_content_type(self):
        headers = self.response.headers
        print(headers)
        content_type = self.response.headers['Content-Type']
        assert ExpectedText.content_type in content_type, \
            logger.warning('The headers Content-Type is wrong')

    def check_date_today(self):
        date_response = self.response.headers['Date'][5:16]
        change_format_date_response = datetime.strptime(date_response, "%d %b %Y")
        change_format_date_response = change_format_date_response.strftime("%Y-%m-%d")
        today = str(datetime.today())[:10]
        assert today == change_format_date_response, \
            logger.warning('The entity creation date does not match the current day')

    def remove_keys(self, d, key):
        if isinstance(d, dict):
            return {k: self.remove_keys(v, key) for k, v in d.items() if k != key}
        elif isinstance(d, list):
            return [self.remove_keys(v, key) for v in d]
        else:
            return d

    def modify_payload(self, new_payload):
        keys_to_remove = ['id', 'verified']
        new_payload = {key: value for key, value in new_payload.items() if key not in keys_to_remove}
        new_payload['addition']['additional_info'] = ''.join(random.choices(string.ascii_letters, k=10))
        return new_payload
