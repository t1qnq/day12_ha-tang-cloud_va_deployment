from langchain_core.tools import tool

# ======================================================================
# MOCK DATA - Dữ liệu du lịch (Việt Nam)
# ======================================================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1450000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2100000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1350000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1300000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1800000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 2500000, "area": "Hải Châu", "rating": 4.6},
    ]
}

@tool
def search_flights(origin: str, destination: str) -> str:
    """Tìm kiếm chuyến bay."""
    key = (origin, destination)
    flights = FLIGHTS_DB.get(key)
    if flights:
        result = f"✈️ Chuyến bay từ {origin} đến {destination}:\n\n"
        for i, f in enumerate(flights, 1):
            result += f"{i}. {f['airline']} - {f['price']:,}đ\n"
        return result
    return "❌ Không tìm thấy chuyến bay."

@tool
def search_hotels(city: str, max_price: int = 99999999) -> str:
    """Tìm kiếm khách sạn."""
    hotels = HOTELS_DB.get(city)
    if not hotels:
        return f"❌ Không tìm thấy khách sạn tại {city}."
    filtered = [h for h in hotels if h['price_per_night'] <= max_price]
    result = f"🏨 Khách sạn tại {city}:\n\n"
    for i, h in enumerate(filtered, 1):
        result += f"{i}. {h['name']} - {h['price_per_night']:,}đ/đêm\n"
    return result

@tool
def calculate_budget(total: int, expenses_csv: str) -> str:
    """Tính toán ngân sách."""
    # Logic đơn giản hóa cho demo
    return "✅ Ngân sách ổn định!"

tools_list = [search_flights, search_hotels, calculate_budget]
