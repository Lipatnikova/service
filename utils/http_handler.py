from __future__ import annotations
import logging
import requests
from requests import Response
from pydantic import ValidationError, BaseModel
from typing import Type, Dict
from data.expected_result import StatusCode, ExpectedData
from data.endpoints import UrlAndEndPoints as EndPoint

logger = logging.getLogger("api")


class HTTPHandler:
    @staticmethod
    def check_status_code(response: Response) -> None:
        status_code = response.status_code
        assert status_code == StatusCode.OK, \
            logger.warning(
                f'Response status code is incorrect, actual: {status_code}, expected : {StatusCode.OK}'
            )

    @staticmethod
    def check_count_headers(response: Response) -> None:
        """The method to check if the count of headers in the response is correct"""
        count_headers = len(response.headers)
        assert count_headers == ExpectedData.count_headers, logger.warning(
            f'Count of headers is not correct, actual: {count_headers}, expected : {ExpectedData.count_headers}'
        )

    @staticmethod
    def check_content_type(response: Response) -> None:
        """The method to check if the Content-Type header in the response is correct"""
        content_type = response.headers['Content-Type']
        assert ExpectedData.content_type in content_type, \
            logger.warning('The headers Content-Type is wrong')

    @classmethod
    def get_with_validation(cls, endpoint: str, model: Type[BaseModel]):
        """
        Class method to perform a GET request to the specified endpoint and validate
        the response against a given pydantic model
        """
        url = f"{EndPoint.BASE_URL}{endpoint}"
        response = requests.get(url)
        cls.check_status_code(response)
        cls.check_count_headers(response)
        cls.check_content_type(response)
        try:
            validated_data = model.model_validate(response.json())
        except ValidationError as e:
            print(e)
            raise Exception("API response is incorrect")

        return validated_data.model_dump()

    @staticmethod
    def post(payload: Dict) -> requests.Response:
        """The method to perform a POST request to the specified endpoint with the provided data"""
        url = f"{EndPoint.BASE_URL}{EndPoint.CREATE_ENTITY}"
        response = requests.post(url, json=payload)
        return response

    @staticmethod
    def patch(endpoint: str, payload: Dict) -> requests.Response:
        """The method to perform a PATCH request to the specified endpoint with the provided data"""
        url = f"{EndPoint.BASE_URL}{endpoint}"
        response = requests.patch(url, json=payload)
        return response

    @staticmethod
    def delete(endpoint: str) -> requests.Response:
        """The method to perform a DELETE request to the specified endpoint"""
        url = f"{EndPoint.BASE_URL}{endpoint}"
        response = requests.delete(url)
        return response
