from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from api.db import Base


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, unique=True)
    blob = Column(String, default="empty")
    user_id = Column(Integer, ForeignKey("users.id"))

    user_system = relationship("User", back_populates="budgets")
