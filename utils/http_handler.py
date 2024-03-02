import requests
import json
import os
from typing import Dict, Any, Optional

from data.endpoints import UrlAndEndPoints as EndPoint
from utils.validator import validator


class HTTPHandler:

    @staticmethod
    def validate_response(response: requests.Response, schemas) -> None:
        """The method to validate a JSON response against a given schema"""
        try:
            response_json = response.json()
            is_valid = validator(response_json, schemas)
            if not is_valid:
                raise Exception("Invalid JSON response")
        except json.JSONDecodeError:
            raise Exception("Invalid JSON response:", json.JSONDecodeError)

    @classmethod
    def get(cls, endpoint: str, schemas: Optional[str] = None,
            params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Class method to perform a GET request to the specified endpoint and validate
        the response against a given schema
        """
        url = f"{EndPoint.BASE_URL}{endpoint}"
        response = requests.get(url, params=params)
        if schemas:
            schemas_path_and_name = os.path.join('..', 'utils', 'schemas', schemas)
            absolute_schemas_path_and_name = os.path.abspath(schemas_path_and_name)
            cls.validate_response(response, absolute_schemas_path_and_name)
        return response

    @classmethod
    def post(cls, endpoint: str, data: Dict[str, Any], schemas: Optional[str] = None) -> requests.Response:
        """
        The method to perform a POST request to the specified endpoint with the provided data
        and validate the response against a given schema
        """
        url = f"{EndPoint.BASE_URL}{endpoint}"
        response = requests.post(url, json=data)
        if schemas:
            schemas_path_and_name = os.path.join('..', 'utils', 'schemas', schemas)
            absolute_schemas_path_and_name = os.path.abspath(schemas_path_and_name)
            cls.validate_response(response, absolute_schemas_path_and_name)
        return response

    @classmethod
    def patch(cls, endpoint: str, data: Dict[str, Any], schemas: Optional[str] = None) -> requests.Response:
        """
         The method to perform a PATCH request to the specified endpoint with the provided data
        and validate the response against a given schema
        """
        url = f"{EndPoint.BASE_URL}{endpoint}"
        response = requests.patch(url, json=data)
        if schemas:
            schemas_path_and_name = os.path.join('..', 'utils', 'schemas', schemas)
            absolute_schemas_path_and_name = os.path.abspath(schemas_path_and_name)
            cls.validate_response(response, absolute_schemas_path_and_name)
        return response

    @classmethod
    def delete(cls, endpoint: str) -> requests.Response:
        """
        The method to perform a DELETE request to the specified endpoint
        and return the response
        """
        url = f"{EndPoint.BASE_URL}{endpoint}"
        response = requests.delete(url)
        return response
