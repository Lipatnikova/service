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
