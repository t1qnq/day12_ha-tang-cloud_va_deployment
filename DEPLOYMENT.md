# Deployment Information - TravelBuddy AI Agent

## Public URL
**[https://day12ha-tang-cloudvadeployment-production-22ec.up.railway.app](https://day12ha-tang-cloudvadeployment-production-22ec.up.railway.app)**

## Platform
- **Cloud Platform**: Railway (App Service)
- **Database**: Railway Redis (Managed Service)
- **Engine**: Docker (Gunicorn + Uvicorn)

## Test Commands

### 1. Health Check
```bash
curl https://day12ha-tang-cloudvadeployment-production-22ec.up.railway.app/health
# Expected Output: {"status":"ok","environment":"production","version":"1.0.0"}
```

### 2. API Chat Test (With Authentication)
```bash
curl -X POST https://day12ha-tang-cloudvadeployment-production-22ec.up.railway.app/chat \
  -H "X-API-Key: travel-secret-123" \
  -H "Content-Type: application/json" \
  -d '{"message": "Chào bạn, hãy gợi ý cho mình một khách sạn ở Đà Nẵng"}'
```

### 3. Security Check (Invalid Key)
```bash
curl -X POST https://day12ha-tang-cloudvadeployment-production-22ec.up.railway.app/chat \
  -H "X-API-Key: wrong-key" \
  -H "Content-Type: application/json" \
  -d '{"message": "Sẽ bị lỗi 403"}'
```

## Environment Variables Set
- `PORT`: 8080 (Railway Managed)
- `REDIS_URL`: redis://... (Railway Managed)
- `AGENT_API_KEY`: travel-secret-123
- `OPENROUTER_API_KEY`: [Encrypted/Protected]
- `ENVIRONMENT`: production
