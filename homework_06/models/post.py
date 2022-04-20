from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from .database import db, Base


class Post(Base, db.Model):
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=False, index=True,)
    title = Column(String(200), nullable=False, default="", server_default="",)
    body = Column(Text, nullable=False, default="", server_default="",)
    user = relationship("User", back_populates="posts")
