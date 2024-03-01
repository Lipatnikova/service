import json
from typing import Any


class FileHandler:
    def write_into_json_file(self, data: Any, file_path: str) -> None:
        """
        Записывает данные в файл в формате JSON.

        Аргументы:
        data (Any): Данные для записи в файл.
        file_path (str): Путь к файлу, в который будут записаны данные.

        Возвращает:
        None
        """
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def read_from_json_file(self, file_path: str) -> Any:
        """
        Читает данные из файла в формате JSON.

        Аргументы:
        file_path (str): Путь к файлу, из которого будут прочитаны данные.

        Возвращает:
        Any: Прочитанные данные из файла.
        """
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
