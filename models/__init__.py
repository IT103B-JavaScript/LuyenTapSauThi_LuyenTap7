"""Gom các model để SQLAlchemy nhận diện đầy đủ quan hệ khi tạo bảng."""
from models.car_type import CarType
from models.car import Car

__all__ = ["CarType", "Car"]
