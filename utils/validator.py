import jsonschema
import json
import logging
from os.path import join, dirname
from jsonschema import Draft202012Validator

logger = logging.getLogger("api")


def validator(data, schema_file):
    """ Checks whether the given data matches the schema.
        Also checks if schema is valid.
    """
    schema = _load_json_schema(schema_file)
    try:
        Draft202012Validator.check_schema(schema)
    except jsonschema.exceptions.SchemaError as e:
        logger.error("JSON Schema is incorrect:", e)
    else:
        return Draft202012Validator(schema).is_valid(data)


def _load_json_schema(filename):
    """ Loads the given schema file """

    relative_path = join('schemas', filename)
    absolute_path = join(dirname(__file__), relative_path)
    try:
        with open(absolute_path) as schema_file:
            try:
                return json.loads(schema_file.read())
            except json.decoder.JSONDecodeError:
                logger.error(f"JSON file has incorrect data: {relative_path}")
    except FileNotFoundError:
        logger.error(f"No such JSON schema file: {relative_path}")
        return False
