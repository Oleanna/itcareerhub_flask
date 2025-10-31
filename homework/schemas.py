from pydantic import BaseModel, Field

class CategoryCreateSchema(BaseModel):
    model_config = {
        "from_attributes": True
    }

    name: str = Field(..., max_length=100)
    description: str = Field(..., max_length=225)


class CategoryResponseSchema(BaseModel):
    model_config = {
        "from_attributes": True
    }

    id: int
    name: str
    description: str


class ProductCreateSchema(BaseModel):
    model_config = {
        "from_attributes": True
    }
    name: str = Field(..., max_length=100)
    price: float
    in_stock: bool
    category_name: str
    category_id: int | None = None


class ProductResponseSchema(BaseModel):
    model_config = {
        "from_attributes": True
    }
    id: int
    name: str
    price: float
    in_stock: bool
    category_id: int

class ProductInfoSchema(BaseModel):
    model_config = {
        "from_attributes": True
    }
    name: str
    price: float


class CategoryWithProductsSchema(BaseModel):
    model_config = {
        "from_attributes": True
    }
    id: int
    name: str
    description: str
    products: list[ProductInfoSchema]

