"""
Router API xe: GET /cars, POST /cars
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.car_schema import CarCreate, CarDetailResponse, CarListResponse
from services import car_service

router = APIRouter(prefix="/cars", tags=["Xe"])


@router.get("", response_model=CarListResponse, status_code=status.HTTP_200_OK)
def get_cars(db: Session = Depends(get_db)):
    """API 2: Truy vấn danh sách xe kèm chi tiết loại xe."""
    items = car_service.get_all_cars(db)
    return {
        "statusCode": 200,
        "error": None,
        "message": "Lấy danh sách xe thành công",
        "data": items,
    }


@router.post("", response_model=CarDetailResponse, status_code=status.HTTP_201_CREATED)
def create_car(payload: CarCreate, db: Session = Depends(get_db)):
    """API 1: Thêm mới một xe."""
    new_item = car_service.create_car(db, payload)
    return {
        "statusCode": 201,
        "error": None,
        "message": "Thêm mới xe thành công",
        "data": new_item,
    }
