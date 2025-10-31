import json
import os
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy import create_engine, select, func
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, joinedload

from hw4_models import Category, Product
from schemas import CategoryCreateSchema, ProductCreateSchema, CategoryWithProductsSchema, ProductInfoSchema, \
    ProductResponseSchema
from homework.db import DBConnector


BASE_DIR: Path = Path(__file__).parent

DB_PATH: Path = BASE_DIR / 'test_database_hw.db'

engine = create_engine(
    url=f"sqlite:///{DB_PATH}",
    echo=True
)

def create_category(session, raw_data):
    try:
        validated_data = CategoryCreateSchema.model_validate_json(raw_data)

        сategory = Category(**validated_data.model_dump())

        session.add(сategory)
        session.commit()

        return CategoryCreateSchema.model_validate(сategory)

    except ValidationError as exc:
        raise ValueError(f"Error: {exc}")

    except (IntegrityError, DataError) as exc:
        session.rollback()

        raise exc

def create_product(session, raw_data):
    try:
        validated_data = ProductCreateSchema.model_validate(raw_data)

        stmt = select(Category).where(Category.name == validated_data.category_name)
        сategory = session.execute(stmt).scalar_one_or_none()

        product_data = validated_data.model_dump()
        product_data['category_id'] = сategory.id
        product_data.pop('category_name')

        product = Product(**product_data)

        session.add(product)
        session.commit()

        return ProductCreateSchema.model_validate(product)

    except ValidationError as exc:
        raise ValueError(f"Error: {exc}")

    except (IntegrityError, DataError) as exc:
        session.rollback()

        raise exc

def get_all_categories_with_products(session):
    # stmt = (
    # select(Category.name, Product.name, Product.price, Category.description)
    # .join(Product, Category.id == Product.category_id, isouter=True)
    #     )
    # result = session.execute(stmt).all()

    stmt = select(Category).options(joinedload(Category.products))
    categories = session.execute(stmt).unique().scalars().all()

    if not categories:
        raise ValueError("Categories not found")

    return [CategoryWithProductsSchema.model_validate(category) for category in categories]
    #return result

def update_product_price(session, product_name: str, new_price: float):
    stmt = select(Product).where(Product.name == product_name)
    product = session.scalars(stmt).first()

    if not product:
        raise ValueError(f"product '{product_name}' not found")

    product.price = new_price

    session.commit()

    return ProductResponseSchema.model_validate(product)

def get_product_count_by_category(session):
    stmt = (
        select(Category.name, func.count(Product.id).label("product_count"))
        .join(Product, Category.id == Product.category_id, isouter=True)
        .group_by(Category.name)
    )

    results = session.execute(stmt).all()

    if not results:
        raise ValueError("Data not found")

    return results

def get_categories_with_multiple_products(session):
    stmt = (
        select(Category.name, func.count(Product.id).label("product_count"))
        .join(Product, Category.id == Product.category_id, isouter=True)
        .group_by(Category.name)
        .having(func.count(Product.id) > 1)
    )

    results = session.execute(stmt).all()

    if not results:
        raise ValueError("Data not found")

    return results

with DBConnector(engine) as session:
    categories = [
        {
            "name": "Одежда",
            "description": "Одежда для мужчин и женщин."
        },
        {
            "name": "Электроника",
            "description": "Гаджеты и устройства."
        },
        {
            "name": "Книги",
            "description": "Печатные книги и электронные книги."
        }
    ]
    json_data = """{
          "name": "Одежда",
          "description": "Одежда для мужчин и женщин."
        }"""

    for data in categories:
        try:
            create_category = create_category(session=session, raw_data=data)

            print(create_category)
        except Exception as err:
            print(f"ERROR: {err}")

with DBConnector(engine) as session:
    products = [
        {
            "name": "Смартфон",
            "price": 299.99,
            "in_stock": True,
            "category_name": "Электроника"
        },
        {
            "name": "Ноутбук",
            "price": 499.99,
            "in_stock": True,
            "category_name": "Электроника"
        },
        {
            "name": "Научно-фантастический роман",
            "price": 15.99,
            "in_stock": True,
            "category_name": "Книги"
        },
        {
            "name": "Джинсы",
            "price": 40.50,
            "in_stock": True,
            "category_name": "Одежда"
        },
        {
            "name": "Джинсы",
            "price": 40.50,
            "in_stock": True,
            "category_name": "Одежда"
        }
    ]

    for data in products:

        try:
            product = create_product(session=session, raw_data=data)

            print(product)
        except Exception as err:
            print(f"ERROR: {err}")


with DBConnector(engine) as session:
    try:
        categories = get_all_categories_with_products(session=session)

        print("CATEGORIES WERE FOUND")
        for data in categories:
            #print(data.model_dump_json(indent=4))
            print(data)
    except ValueError as exc:
        print(exc)

with DBConnector(engine) as session:
    try:
        updated_product = update_product_price(session, "Смартфон", 349.99)

        print("PRODUCT WAS UPDATED")
        print(updated_product.model_dump_json(indent=4))
    except ValueError as exc:
        print(exc)

with DBConnector(engine) as session:
    try:
        results = get_product_count_by_category(session)
        #results = get_categories_with_multiple_products(session)

        print("PRODUCT COUNT BY CATEGORY:")
        for result in results:
            print(result)
    except ValueError as exc:
        print(exc)