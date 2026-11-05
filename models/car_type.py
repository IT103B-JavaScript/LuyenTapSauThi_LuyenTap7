"""
Model bảng car_types (loại xe) - phía "1" của quan hệ 1-N.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class CarType(Base):
    __tablename__ = "car_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)

    # Một loại xe có nhiều xe
    cars = relationship("Car", back_populates="car_type")
