from datetime import datetime
from typing import Optional, List, Self

from pydantic import Field, model_validator

from src.dtos.base import BaseDTO, IDMixin, TimestampMixin



class CategoryBase(BaseDTO):
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

class CategoryCreateRequest(CategoryBase):
    ...

class CategoryUpdateRequest(CategoryBase):
    ...

class CategoryResponse(IDMixin, TimestampMixin):
    name: str
