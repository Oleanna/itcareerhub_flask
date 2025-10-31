from pathlib import Path
from typing import Optional
from sqlalchemy import String, Integer, create_engine, ForeignKey, Text, Table, Column, Float, Boolean
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship, declarative_base
)

from homework.hw4 import engine

Base = declarative_base()

class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

class Product(Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    in_stock: Mapped[bool] = mapped_column(Boolean)
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.id")
    )

    categories: Mapped["Category"] = relationship(
        "Category",
        back_populates="products"
    )


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))

    products: Mapped[list["Product"]] = relationship("Product", back_populates="categories")


Base.metadata.create_all(bind=engine)