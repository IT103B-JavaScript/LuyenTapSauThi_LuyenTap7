"""
Service xử lý nghiệp vụ xe.
"""
from sqlalchemy.orm import Session, joinedload

from models.car import Car
from models.car_type import CarType
from schemas.car_schema import CarCreate
from utils.exceptions import AppException


def get_all_cars(db: Session):
    """Lấy toàn bộ xe kèm thông tin loại xe."""
    return (
        db.query(Car)
        .options(joinedload(Car.car_type))
        .order_by(Car.id)
        .all()
    )


def create_car(db: Session, payload: CarCreate) -> Car:
    """Thêm mới xe: kiểm tra loại xe tồn tại và mã xe không bị trùng."""
    type_obj = db.get(CarType, payload.car_type_id)
    if type_obj is None:
        raise AppException(
            404, "Not Found",
            f"Không tìm thấy loại xe có id = {payload.car_type_id}",
        )

    duplicated = db.query(Car).filter(Car.car_code == payload.car_code).first()
    if duplicated is not None:
        raise AppException(
            409, "Conflict",
            f"Mã xe {payload.car_code} đã tồn tại",
        )

    new_car = Car(**payload.model_dump())
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car
