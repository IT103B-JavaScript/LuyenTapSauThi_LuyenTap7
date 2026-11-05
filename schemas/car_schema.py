"""
Schemas Pydantic: validate dữ liệu đầu vào và định nghĩa cấu trúc dữ liệu đầu ra.
"""
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CarTypeResponse(BaseModel):
    """Thông tin loại xe trả về kèm trong xe."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class CarCreate(BaseModel):
    """Dữ liệu đầu vào khi thêm mới xe."""
    car_code: str = Field(..., min_length=4, max_length=10, examples=["C010"])
    daily_rate: float = Field(..., gt=0, examples=[800000])
    car_type_id: int = Field(..., examples=[1])

    @field_validator("car_code")
    @classmethod
    def normalize_code(cls, value: str) -> str:
        """Bỏ khoảng trắng hai đầu, chuyển in hoa và kiểm tra lại độ dài."""
        value = value.strip().upper()
        if len(value) < 4:
            raise ValueError("Mã xe phải có ít nhất 4 ký tự")
        return value


class CarResponse(BaseModel):
    """Thông tin xe trả về (dùng làm response_model)."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    car_code: str
    daily_rate: float
    car_type: CarTypeResponse


class CarListResponse(BaseModel):
    """Response chuẩn cho API lấy danh sách xe."""
    statusCode: int
    error: Optional[str] = None
    message: str
    data: List[CarResponse]


class CarDetailResponse(BaseModel):
    """Response chuẩn cho API trả về một xe."""
    statusCode: int
    error: Optional[str] = None
    message: str
    data: CarResponse


class CarTypeDeleteResponse(BaseModel):
    """Response chuẩn cho API xóa loại xe."""
    statusCode: int
    error: Optional[str] = None
    message: str
    data: Optional[CarTypeResponse] = None
