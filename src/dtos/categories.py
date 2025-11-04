from datetime import datetime
from typing import Optional, List, Self

from pydantic import Field, model_validator

from src.dtos.base import BaseDTO, IDMixin, TimestampMixin


class CategoryCreateRequest(BaseDTO):
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

class CategoryUpdateRequest(BaseDTO):
    name: str = Field(
        None,
        min_length=1,
        max_length=255,
    )

class CategoryResponse(IDMixin, TimestampMixin):
    name: str
