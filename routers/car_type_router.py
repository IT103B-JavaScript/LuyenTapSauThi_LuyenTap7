"""
Router API loại xe: DELETE /car-types/{id}
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.car_schema import CarTypeDeleteResponse
from services import car_type_service

router = APIRouter(prefix="/car-types", tags=["Loại xe"])


@router.delete("/{id}", response_model=CarTypeDeleteResponse, status_code=status.HTTP_200_OK)
def delete_car_type(id: int, db: Session = Depends(get_db)):
    """API 3: Xóa loại xe theo ID (chỉ khi không còn xe thuộc loại này)."""
    deleted = car_type_service.delete_car_type(db, id)
    return {
        "statusCode": 200,
        "error": None,
        "message": f"Xóa loại xe '{deleted.name}' thành công",
        "data": deleted,
    }
