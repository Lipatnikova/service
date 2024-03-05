"""This file contains models for pydantic JSON validation"""
from __future__ import annotations
from typing import List
from pydantic import (BaseModel)


class AdditionModel(BaseModel):
    id: int
    additional_info: str
    additional_number: int


class EntityModel(BaseModel):
    id: int
    title: str
    verified: bool
    addition: AdditionModel
    important_numbers: List[int]


class EntitiesModel(BaseModel):
    entity: List[EntityModel]
