"""
Service xử lý nghiệp vụ loại xe.
"""
from sqlalchemy.orm import Session

from models.car import Car
from models.car_type import CarType
from utils.exceptions import AppException

DEFAULT_CAR_TYPES = ["sedan", "suv", "pickup"]


def seed_default_car_types(db: Session) -> None:
    """Tạo sẵn các loại xe mặc định nếu bảng đang trống (phục vụ test API)."""
    if db.query(CarType).count() > 0:
        return
    for type_name in DEFAULT_CAR_TYPES:
        db.add(CarType(name=type_name))
    db.commit()


def delete_car_type(db: Session, type_id: int) -> CarType:
    """Xóa loại xe theo id, chỉ cho phép khi không còn xe nào thuộc loại này."""
    type_obj = db.get(CarType, type_id)
    if type_obj is None:
        raise AppException(404, "Not Found", f"Không tìm thấy loại xe có id = {type_id}")

    total_cars = db.query(Car).filter(Car.car_type_id == type_id).count()
    if total_cars > 0:
        raise AppException(
            400, "Bad Request",
            f"Không thể xóa loại xe '{type_obj.name}' vì còn {total_cars} xe thuộc loại này",
        )

    db.delete(type_obj)
    db.commit()
    return type_obj
