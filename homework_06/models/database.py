__all__ = ("db", "Base")

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Integer
from sqlalchemy.orm import declared_attr

db = SQLAlchemy()


class Base:

    @declared_attr
    def __tablename__(cls):
        print(f"{cls.__name__.lower()}s")
        return f"{cls.__name__.lower()}s"

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return str(self)
