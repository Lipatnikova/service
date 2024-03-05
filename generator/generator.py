import random
import string
from dataclasses import dataclass, field
from faker import Faker

fake = Faker()


@dataclass
class Payload:
    additional_info: str = field(default=fake.first_name())
    additional_number: int = field(default=fake.random_number(digits=3))
    important_numbers: list = field(default_factory=lambda: [fake.random_number(digits=2) for _ in range(3)])
    title: str = field(default=f"Заголовок сущности {fake.first_name()}")
    verified: bool = field(default=fake.boolean())

    def to_dict(self):
        return {
            "addition": {
                "additional_info": self.additional_info,
                "additional_number": self.additional_number
            },
            "important_numbers": self.important_numbers,
            "title": self.title,
            "verified": self.verified
        }

    def to_dict_patch(self):
        return {
            "addition": {
                "additional_info": self.additional_info,
                "additional_number": self.additional_number
            }
        }


def generate_payload():
    return Payload().to_dict()


def modify_payload(new_payload):
    """The method to modify a payload by removing specified keys and adding additional information"""
    keys_to_remove = ['id', 'verified']
    new_payload = {key: value for key, value in new_payload.items() if key not in keys_to_remove}
    new_payload['addition']['additional_info'] = ''.join(random.choices(string.ascii_letters, k=10))
    return new_payload
