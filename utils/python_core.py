"""
Phần 1: Python Core & Tư duy thuật toán
- Yêu cầu 1.1: clean_and_validate_cars
- Yêu cầu 1.2: search_cars (Linear Search)
- Yêu cầu 1.3: sort_cars_by_daily_rate_desc (Bubble Sort)
Chạy thử: python -m utils.python_core
"""

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


def is_valid_car_code(code):
    """Mã hợp lệ: bắt đầu bằng chữ cái C, theo sau là ít nhất một chữ số (chỉ chữ số)."""
    return len(code) >= 2 and code[0] == "C" and code[1:].isdigit()


def clean_and_validate_cars(raw_list):
    """Yêu cầu 1.1: chuẩn hóa car_code (strip + upper) và loại bỏ xe có mã không hợp lệ."""
    cleaned_list = []
    for item in raw_list:
        code = str(item.get("car_code", "")).strip().upper()
        if is_valid_car_code(code):
            cleaned_item = dict(item)  # tạo bản sao, không sửa dữ liệu gốc
            cleaned_item["car_code"] = code
            cleaned_list.append(cleaned_item)
        else:
            print(f"[Loại bỏ] mã xe không hợp lệ: {item.get('car_code')!r}")
    return cleaned_list


def search_cars(item_list, max_daily_rate, status=None):
    """Yêu cầu 1.2: tìm tuyến tính xe có daily_rate <= max_daily_rate và đúng status (None = bỏ qua status)."""
    result = []
    for item in item_list:
        if item["daily_rate"] > max_daily_rate:
            continue
        if status is not None and item["status"] != status:
            continue
        result.append(item)
    return result


def sort_cars_by_daily_rate_desc(item_list):
    """Yêu cầu 1.3: Bubble Sort giảm dần theo daily_rate, trả về danh sách mới."""
    sorted_list = list(item_list)
    n = len(sorted_list)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if sorted_list[j]["daily_rate"] < sorted_list[j + 1]["daily_rate"]:
                sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]
                swapped = True
        if not swapped:
            break
    return sorted_list


def print_cars(title, item_list):
    """In danh sách xe dạng bảng để kiểm tra kết quả."""
    print(f"\n===== {title} ({len(item_list)}) =====")
    for item in item_list:
        print(
            f"{item['car_code']:<8} | {item['type']:<14} | "
            f"{item['daily_rate']:>12,} | {item['status']}"
        )


if __name__ == "__main__":
    valid_cars = clean_and_validate_cars(raw_cars)
    print_cars("1.1 Sau khi chuẩn hóa & validate", valid_cars)

    print_cars(
        "1.2 Tìm xe có daily_rate <= 1000000 và status = 'available'",
        search_cars(valid_cars, 1000000, "available"),
    )
    print_cars(
        "1.2 Tìm xe có daily_rate <= 1000000 (status = None)",
        search_cars(valid_cars, 1000000),
    )

    print_cars("1.3 Sắp xếp daily_rate giảm dần (Bubble Sort)", sort_cars_by_daily_rate_desc(valid_cars))
