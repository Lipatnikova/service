import os


class UrlAndEndPoints:

    BASE_URL = os.getenv("BASE_URL")

    ENTITIES = "api/getAll"
    ENTITY = f"api/get/"
    DEL_ENTITY = f"api/delete/"
    CREATE_ENTITY = "api/create"
    CHANGE_ENTITY = f"api/patch/"
