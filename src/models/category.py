from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, TimestampMixin


class Category(Base, TimestampMixin):
    __tablename__ = 'categories'

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    polls: Mapped[list["Poll"]] = relationship(back_populates="category")