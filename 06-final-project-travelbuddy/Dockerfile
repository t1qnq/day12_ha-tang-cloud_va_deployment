FROM python:3.11-slim

# Cài đặt các thư viện hệ thống cần thiết
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Cài đặt dependencies ngay tại stage này
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn
COPY . .

# Đảm bảo PYTHONPATH trỏ đúng vào thư mục gốc của app
ENV PYTHONPATH=/app

# Railway sẽ tự động truyền biến PORT, chúng ta sử dụng biến đó
EXPOSE 8000

# Lệnh khởi động linh hoạt hơn
CMD ["python", "-m", "app.main"]
