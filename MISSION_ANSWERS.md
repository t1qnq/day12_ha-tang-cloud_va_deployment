# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Phát hiện anti-patterns
Qua phân tích mã nguồn `01-localhost-vs-production/develop/app.py`, tôi đã phát hiện 8 vấn đề (anti-patterns) nghiêm trọng ngăn cản ứng dụng chạy ổn định ở môi trường Production:

1.  **Hardcoded Secrets:** API Key (`OPENAI_API_KEY`) nằm trực tiếp trong code.
2.  **Environment Inconsistency:** Không sử dụng biến môi trường, dẫn đến xung đột thư viện.
3.  **Hardcoded Host/Port:** Fix cứng `localhost` và cổng `8000`.
4.  **Improper Logging:** Sử dụng `print()` thay vì structured logging.
5.  **No Health Checks:** Thiếu `/health` endpoint để platform giám sát.
6.  **Active Reloader:** Bật `reload=True` ở production gây rủi ro bảo mật.
7.  **Thiếu Input Validation:** Dẫn đến lỗi 422 khi khách hàng gửi dữ liệu sai định dạng.
8.  **Thiếu Error Handling:** Trả về lỗi 500 chung chung khi gặp sự cố import.

### Exercise 1.2: Chạy basic version (Observation)
- **Kết quả:** App chạy được nhưng rất "dễ vỡ". Khi test bằng JSON Body, app báo lỗi 422 vì nó chỉ nhận query parameters.
- **Kết luận:** Phiên bản này **KHÔNG** production-ready.

### Exercise 1.3: So sánh với advanced version

| Feature | Basic (Develop) | Advanced (Production) | Tại sao quan trọng? |
|---------|-----------------|-----------------------|---------------------|
| **Config** | Hardcode | Env vars (.env) | Bảo mật và linh hoạt thay đổi môi trường. |
| **Health check** | ❌ Không có | ✅ Có (/health) | Để platform tự động restart khi app treo. |
| **Logging** | print() | JSON Structured | Dễ dàng quản trị và phân tích lỗi tập trung. |
| **Shutdown** | Đột ngột | Graceful | Đảm bảo hoàn tất các request đang xử lý trước khi tắt. |

---

## Part 2: Docker Containerization

### Exercise 2.1: Dockerfile cơ bản
1. **Base image là gì?** Là môi trường nền tảng (OS + Runtime) ban đầu (ví dụ: `python:3.11`).
2. **Working directory là gì?** Là thư mục làm việc mặc định bên trong container.
3. **Tại sao COPY requirements.txt trước?** Để tận dụng **Layer Caching**, không phải cài lại thư viện nếu dependencies không đổi.
4. **CMD vs ENTRYPOINT?** `CMD` là lệnh mặc định (có thể ghi đè), `ENTRYPOINT` là lệnh chính (khó ghi đè).

### Exercise 2.2: Build và run
- **Image Name:** `my-agent:develop` | **Dung lượng:** **1.66 GB**.
- **Nhận xét:** Quá nặng do chứa nhiều file rác từ quá trình biên dịch.

### Exercise 2.3: Multi-stage build
- **Stage 1 (Builder):** Cài tools và biên dịch thư viện.
- **Stage 2 (Runtime):** Chỉ copy các file cần thiết sang bản `slim`.
- **Dung lượng:** **236 MB** (Giảm ~85%).

### Exercise 2.4: Docker Compose stack
- **Services:** Agent, Redis, Qdrant, Nginx.
- **Communication:** Giao tiếp qua tên service (Docker DNS).
- **Kết quả test:** URL `http://localhost/health` trả về `status: ok` qua cổng 80 của Nginx.

---

## Part 3: Cloud Deployment

### Exercise 3.1: Railway deployment
- **URL thực tế:** `https://day12ha-tang-cloudvadeployment-production-e653.up.railway.app`
- **Xác thực:** Đã test thành công cả `/health` và `/ask`.

### Exercise 3.2: Config comparison
- **Railway (railway.toml):** Cấu hình nhanh cho từng dịch vụ đơn lẻ.
- **Render (render.yaml):** Quản lý cả một hệ thống phức tạp (Infrastructure as Code).

---

## Part 4: API Security

### Exercise 4.1 & 4.2: Authentication
- **Cơ chế:** Sử dụng JWT (JSON Web Token) cho phép xác thực không trạng thái (stateless).
- **API Key:** Dùng cho B2B đơn giản; **JWT:** Dùng cho ứng dụng web/mobile chuyên nghiệp.

### Exercise 4.3: Rate Limiting
- **Algorithm:** **Sliding Window Counter** (Dùng `deque` để lưu timestamps).
- **Limit:** 10 requests/phút cho User thường, 100 requests/phút cho Admin.
- **Bypass admin:** Check `role` trong JWT payload, nếu là `admin` thì trỏ ra bộ lọc `rate_limiter_admin`.

### Exercise 4.4: Cost Guard
- **Logic:** Mỗi user có budget theo ngày (mặc định $1/ngày).
- **Cơ chế:** Trước khi gọi LLM, server check usage trong memory (hoặc Redis). Nếu `total_cost >= budget`, trả về **402 Payment Required**.

---

## Part 5: Scaling & Reliability

### Exercise 5.1: Health vs Readiness
- **Health (/health):** Kiểm tra xem process còn sống không (Liveness).
- **Ready (/ready):** Kiểm tra xem app đã kết nối đủ DB/Redis chưa trước khi nhận traffic.

### Exercise 5.2: Graceful Shutdown
- **Cơ chế:** Lắng nghe tín hiệu `SIGTERM`. Khi nhận được, app ngừng nhận request mới, hoàn tất các request cũ rồi mới đóng connection.

### Exercise 5.3: Stateless Design
- **Tại sao?** Để có thể chạy nhiều instance song song. Nếu lưu session trong memory, khi Load Balancer chuyển user sang instance khác, họ sẽ bị mất dữ liệu. **Giải pháp:** Lưu session/history vào Redis.

### Exercise 5.4 & 5.5: Load Balancing & Stateless Test (Dữ liệu thực tế)
- **Cấu hình:** Chạy 3 Agent instances song song kết hợp Redis và Nginx.
- **Kết quả điều phối traffic:** Hệ thống đã tự động phân phối các yêu cầu đến 3 node khác nhau:
    - Node 1: `instance-4abe97`
    - Node 2: `instance-a46754`
    - Node 3: `instance-641185`
- **Xác nhận tính Stateless:** Dù instance xử lý thay đổi liên tục, nhưng nhờ có Redis dùng chung, **Session history** vẫn được bảo toàn nguyên vẹn 100%. Điều này cho phép hệ thống mở rộng không giới hạn mà không làm gián đoạn trải nghiệm người dùng.

---

---

## Part 6: Final Project - TravelBuddy Pro

### 6.1 Tổng quan kiến trúc
Dự án đã được chuyển đổi hoàn toàn sang mô hình **Stateless Architecture**:
- **Backend:** FastAPI với cơ chế Dependency Injection để quản lý Auth và Settings.
- **Session:** Sử dụng **Redis Shared Store** (Railway Managed) để lưu trữ lịch sử hội thoại, cho phép mở rộng không hạn chế.
- **Agent:** Sử dụng LangGraph với bộ công cụ (Tools) tích hợp tìm kiếm vé máy bay và khách sạn.

### 6.2 Bảo mật và Vận hành Cloud
- **Security:** Đã triển khai lớp bảo vệ API Key thủ công qua Header `X-API-Key`.
- **Monorepo Handling:** Sử dụng file `railway.json` tại thư mục gốc để chỉ định chính xác build context cho thư mục `06-final-project-travelbuddy`.
- **Deployment:** [https://day12ha-tang-cloudvadeployment-production-22ec.up.railway.app](https://day12ha-tang-cloudvadeployment-production-22ec.up.railway.app)

### 6.3 Kết luận
Dự án đã đạt trạng thái **Production-Ready**, đáp ứng đầy đủ các tiêu chuẩn về bảo mật, hiệu năng (image size < 250MB) và khả năng mở rộng ngang.
