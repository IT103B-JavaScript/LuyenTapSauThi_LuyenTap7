"""
Model bảng cars (xe) - phía "N" của quan hệ 1-N.
"""
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, autoincrement=True)
    car_code = Column(String(10), unique=True, nullable=False)
    daily_rate = Column(Float, nullable=False)
    car_type_id = Column(Integer, ForeignKey("car_types.id"), nullable=False)

    # Mỗi xe thuộc về một loại xe
    car_type = relationship("CarType", back_populates="cars")
