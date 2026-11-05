# ĐÁNH GIÁ CHẤT LƯỢNG KỸ NĂNG – PYTHON, FASTAPI VÀ DATABASE
## KIỂM TRA ĐÁNH GIÁ NĂNG LỰC CNTT – [Mã đề: 009]
**THỜI GIAN: 90 phút**

---

## Yêu cầu
Tạo project folder theo hướng dẫn sau:
- Tạo folder [Mã Lớp]\_[Họ Tên]\_[Mã Đề] chứa toàn bộ file mã nguồn. *Ví dụ: HN_KS25_CNTT1_NguyenVanA_9*
- Sau khi hoàn thành project, đẩy code lên GitHub và nộp link cho người phụ trách.
- Công nghệ & công cụ sử dụng: Python core + FastAPI + MySQL + SQLAlchemy ORM, Visual Studio Code.

## Thực hành

### 1. Bối cảnh
Hệ thống Quản lý Cho thuê xe tự lái (car_rental_management) cần xây dựng các chức năng xử lý dữ liệu xe bằng Python Core, cấu hình dữ liệu đầu vào/đầu ra với Pydantic, kết nối cơ sở dữ liệu MySQL và viết các API quản lý xe (cars) và loại xe (car_types).

Sinh viên cần xây dựng API quản lý xe, cho phép thêm mới xe, xem danh sách xe kèm chi tiết loại xe, và xóa loại xe kèm xử lý ràng buộc đặc biệt.

### 2. Tài liệu

#### 2.1 Dữ liệu xe (dùng cho Phần 1)
Cho trước danh sách dữ liệu thô chứa thông tin các xe giả định sau:
```python
raw_cars = [
    {"car_code": "C001", "type": "sedan",
     "daily_rate": 800000, "status": "available"},
    {"car_code": " c002 ", "type": "suv",
     "daily_rate": 1200000, "status": "rented"},
    {"car_code": "C003", "type": "pickup",
     "daily_rate": 1000000, "status": "available"},
    {"car_code": "CAR-4", "type": "sedan",
     "daily_rate": 750000, "status": "available"},
    {"car_code": "C005", "type": "suv",
     "daily_rate": 1500000, "status": "maintenance"},
    {"car_code": "C006", "type": "sedan",
     "daily_rate": 900000, "status": "available"}
]
```

#### 2.2 Cơ sở dữ liệu
Database đặt tên là: **car_rental_db**

**Bảng car_types:**
| Trường | Kiểu dữ liệu | Mô tả |
|---|---|---|
| **id** | int | Mã loại xe, khóa chính, tự tăng |
| **name** | string | Tên loại xe, tối đa 50 ký tự, độc nhất, không trống |

**Bảng cars:**
| Trường | Kiểu dữ liệu | Mô tả |
|---|---|---|
| **id** | int | Mã định danh xe, khóa chính, tự tăng |
| **car_code** | string | Mã xe, tối đa 10 ký tự, độc nhất, không trống |
| **daily_rate** | float | Giá thuê theo ngày, không trống |
| **car_type_id** | int | Khóa ngoại liên kết tới bảng car_types |

#### 2.3 Bảng danh sách API
| STT | Chức năng | Method | Endpoint |
|---|---|---|---|
| 1 | Truy vấn danh sách xe | GET | /cars |
| 2 | Thêm xe mới | POST | /cars |
| 3 | Xóa loại xe | DELETE | /car-types/{id} |

#### 2.4 Quy chuẩn cấu trúc Response chung
Tất cả các API bắt buộc phải trả về dữ liệu dưới dạng đồng nhất gồm 4 trường sau:
- **statusCode** (số nguyên): mã trạng thái HTTP (200, 201, 404, ...).
- **error** (chuỗi hoặc null): lỗi nếu có (ví dụ: "Not Found").
- **message** (chuỗi): thông báo trạng thái thực hiện hành động cho người dùng.
- **data** (object/mảng hoặc null): dữ liệu kết quả trả về từ database.

**Ví dụ mẫu Response API lấy danh sách xe thành công:**
```json
{
  "statusCode": 200,
  "error": null,
  "message": "Lấy danh sách xe thành công",
  "data": [
    {
      "id": 1,
      "car_code": "C001",
      "daily_rate": 800000.0,
      "car_type": {
        "id": 1,
        "name": "sedan"
      }
    }
  ]
}
```

### 3. Yêu cầu nghiệp vụ

#### Phần 1: Python Core & Tư duy thuật toán (35 điểm)
**Yêu cầu 1.1 (10 điểm) – Chuẩn hóa & validate dữ liệu:**
Viết hàm `clean_and_validate_cars` thực hiện:
- Loại bỏ khoảng trắng thừa ở hai đầu của mã xe `car_code` và chuyển toàn bộ chữ cái thành dạng in hoa (ví dụ: " c002 " → "C002").
- Kiểm tra tính hợp lệ của mã xe sau khi chuẩn hóa: phải bắt đầu bằng chữ cái C, theo sau là các chữ số. Nếu không hợp lệ, loại bỏ xe đó khỏi danh sách.

**Yêu cầu 1.2 (12 điểm) – Tìm kiếm tuyến tính (Linear Search):**
Viết hàm `search_cars` để tìm kiếm các xe thỏa mãn đồng thời:
- Giá thuê theo ngày (`daily_rate`) nhỏ hơn hoặc bằng giá trị truyền vào tham số.
- Trạng thái (`status`) trùng khớp với giá trị truyền vào tham số (nếu giá trị truyền vào là None thì chỉ lọc theo giá thuê theo ngày).

**Yêu cầu 1.3 (13 điểm) – Sắp xếp nổi bọt (Bubble Sort):**
Viết hàm `sort_cars_by_daily_rate_desc` tự cài đặt thuật toán Bubble Sort để sắp xếp danh sách xe theo thứ tự giá thuê theo ngày giảm dần.

#### Phần 2: Parameter & Pydantic Validation (10 điểm)
**Yêu cầu 2.1 (5 điểm) – Định nghĩa Schema & validate dữ liệu:**
Tạo Schema `CarCreate` để validate dữ liệu đầu vào:
- `car_code`: bắt buộc, độ dài tối thiểu 4 ký tự, tối đa 10 ký tự.
- `daily_rate`: bắt buộc, giá trị phải lớn hơn 0.
- `car_type_id`: bắt buộc (ID liên kết với bảng loại xe).

**Yêu cầu 2.2 (5 điểm) – Phản hồi chuẩn RESTful & Response Model:**
Tạo Schema `CarResponse` dùng làm response_model khi trả về thông tin xe.

#### Phần 3: Kết nối MySQL & SQLAlchemy ORM (20 điểm)
**Yêu cầu 3.1 (10 điểm) – Khai báo cấu hình CSDL:**
Viết file `database.py` kết nối tới cơ sở dữ liệu MySQL local có tên car_rental_db.

**Yêu cầu 3.2 (10 điểm) – Thiết kế Model quan hệ 1-N:**
Khai báo 2 SQLAlchemy Models trong thư mục `models/` đại diện cho mối quan hệ 1-N:
- Bảng car_types: tạo các cột tương ứng, thiết lập mối quan hệ.
- Bảng cars: tạo các cột tương ứng, thiết lập mối quan hệ.

#### Phần 4: Endpoints API & logic nghiệp vụ (35 điểm)
**Yêu cầu 4.1 (5 điểm) – Chia thư mục/file:** Chia thư mục/file theo cấu trúc phân tầng nêu ở mục 5. Yêu cầu kỹ thuật.

**Yêu cầu 4.2 (10 điểm) – API 1: POST /cars**
- **Mô tả:** thêm mới một xe.
- **Yêu cầu:** thêm dữ liệu xe từ Request Body vào database; xử lý trường hợp `car_type_id` không tồn tại và `car_code` bị trùng.

**Yêu cầu 4.3 (10 điểm) – API 2: GET /cars**
- **Mô tả:** truy vấn danh sách xe.
- **Yêu cầu:** trả về danh sách xe kèm theo thông tin chi tiết của loại xe đó.

**Yêu cầu 4.4 (10 điểm) – API 3: DELETE /car-types/{id}**
- **Mô tả:** xóa loại xe theo ID.
- **Yêu cầu:** chỉ cho phép xóa khi không có xe nào thuộc loại xe này.

### 4. Thang điểm chi tiết
| STT | Nghiệp vụ cần đạt được | Mô tả chi tiết nghiệp vụ | Điểm |
|---|---|---|---|
| 1 | Phần 1 – Python Core & Tư duy thuật toán | Yêu cầu 1.1 – Chuẩn hóa & validate dữ liệu: 10 • Yêu cầu 1.2 – Tìm kiếm tuyến tính: 12 • Yêu cầu 1.3 – Sắp xếp nổi bọt: 13 | 35 |
| 2 | Phần 2 – Parameter & Pydantic Validation | Yêu cầu 2.1 – Schema CarCreate & validate dữ liệu: 5 • Yêu cầu 2.2 – Schema CarResponse & response_model: 5 | 10 |
| 3 | Phần 3 – Kết nối MySQL & SQLAlchemy ORM | Yêu cầu 3.1 – Cấu hình kết nối CSDL (database.py): 10 • Yêu cầu 3.2 – Model quan hệ 1-N: 10 | 20 |
| 4 | Phần 4 – Endpoints API & logic nghiệp vụ | Yêu cầu 4.1 – Chia thư mục/file: 5 • Yêu cầu 4.2 – API POST /cars: 10 • Yêu cầu 4.3 – API GET /cars: 10 • Yêu cầu 4.4 – API DELETE /car-types/{id}: 10 | 35 |
| | **Tổng cộng** | | **100** |

### 5. Yêu cầu kỹ thuật
- Chạy được chương trình bằng lệnh `uvicorn main:app --reload`.
- Test được API trên Swagger UI.
- Kết nối được FastAPI với MySQL thông qua SQLAlchemy ORM.
- Source code được tách thành nhiều file theo cấu trúc phân tầng rõ ràng và hợp lý.

*Lưu ý: Chỉ tính điểm khi chức năng chương trình thực hiện đúng theo yêu cầu nghiệp vụ được giao.*

---

## Hướng dẫn chạy bài giải mẫu (thư mục `car_rental_management/`)
```
car_rental_management/
├── main.py                     # khởi tạo app, đăng ký router, xử lý lỗi
├── database.py                 # kết nối MySQL car_rental_db
├── models/
│   ├── __init__.py
│   ├── car_type.py
│   └── car.py
├── schemas/
│   ├── __init__.py
│   └── car_schema.py
├── services/
│   ├── __init__.py
│   ├── car_service.py
│   └── car_type_service.py
├── routers/
│   ├── __init__.py
│   ├── car_router.py
│   └── car_type_router.py
├── utils/
│   ├── __init__.py
│   ├── python_core.py          # Phần 1
│   ├── exceptions.py
│   └── response.py
├── create_database.sql
└── requirements.txt
```
1. `pip install -r requirements.txt`
2. Chạy `create_database.sql` trong MySQL (tạo database `car_rental_db`), sửa user/mật khẩu trong `database.py` nếu khác `root/123456`.
3. Phần 1: `python -m utils.python_core`
4. API: `uvicorn main:app --reload` → mở http://127.0.0.1:8000/docs. Khi khởi động, bảng `car_types` được tạo sẵn các loại: 1 = sedan, 2 = suv, 3 = pickup.
