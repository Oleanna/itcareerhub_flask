from pydantic import BaseModel, Field, EmailStr, field_validator
from pydantic_core.core_schema import ValidationInfo


class Address(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: int = Field(gt=0)

class User(BaseModel):

    name: str = Field(min_length=2, pattern=r'^[a-zA-Z\s]+$')
    age: int = Field(ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @field_validator("is_employed")
    def check_age(cls, value: bool, info: ValidationInfo):
        age = info.data.get('age')
        if value and not (18 <= age <= 65):
            raise ValueError('If user is employed, age must be between 18 and 65')

        return value


json_input = """{
    "name": "John Doe",
    "age": 60,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""

json_invalid = """{
    "name": "12",
    "age": 17,
    "email": "john.doeexample.com",
    "is_employed": true,
    "address": {
        "city": "N",
        "street": "5t",
        "house_number": -1
    }
}"""


user = User.model_validate_json(json_input)
print(user.model_dump_json(indent=4))
