from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .database import db, Base


class User(db.Model, Base):
    name = Column(String(128), nullable=False)
    username = Column(String(32), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    posts = relationship("Post", back_populates="user", cascade="all, delete")

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name!r}>"
