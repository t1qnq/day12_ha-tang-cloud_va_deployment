#  Delivery Checklist — Day 12 Lab Submission

> **Student Name:** Quách Ngọc Quang  
> **Student ID:** 2A202600285 
> **Date:** 17/04/2026

---

##  Submission Requirements

Submit a **GitHub repository** containing:

### 1. Mission Answers (40 points)

- [x] MISSION_ANSWERS.md completed.

Create a file `MISSION_ANSWERS.md` with your answers to all exercises:

```markdown
# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Phát hiện anti-patterns
1. **Hardcoded Secrets:** API Key nằm trực tiếp trong code.
2. **Hardcoded Host/Port:** Fix cứng localhost và cổng 8000.
3. **No Health Checks:** Thiếu /health endpoint để giám sát.
... (Xem chi tiết tại MISSION_ANSWERS.md)

### Exercise 1.3: Comparison table
| Feature | Basic (Develop) | Advanced (Production) | Tại sao quan trọng? |
|---------|-----------------|-----------------------|---------------------|
| **Config** | Hardcode | Env vars (.env) | Bảo mật và linh hoạt. |
| **Health** | ❌ Không có | ✅ Có (/health) | Tự động restart. |

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. Base image: python:3.11-slim (Tối ưu kích thước).
2. Working directory: /app (Tiêu chuẩn).
3. Caching: COPY requirements.txt trước để tận dụng Layer Cache.

### Exercise 2.3: Image size comparison
- Develop: 1.66 GB
- Production: 236 MB
- Difference: Giảm ~85%

## Part 3: Cloud Deployment

### Exercise 3.1: Railway deployment
- URL: https://day12ha-tang-cloudvadeployment-production-22ec.up.railway.app
- Status: Deployment hoàn tất và hoạt động ổn định.

## Part 4: API Security

### Exercise 4.1-4.3: Test results
- Auth check: 200 OK with valid key.
- Security check: 403 Forbidden with invalid key.

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes
- Stateless: Dùng Redis lưu session history.
- Scaling: Chạy 3 instances Agent điều phối bởi Nginx.
```

---

### 2. Full Source Code - Lab 06 Complete (60 points)

- [x] Full source code for Part 6 implemented.

Your final production-ready agent with all files:

```
day12-ha-tang-cloud/
├── 06-final-project-travelbuddy/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── agent.py             # LangGraph logic
│   │   └── config.py            # Pydantic Settings
│   ├── Dockerfile               # Optimized build
│   ├── requirements.txt         # Deps
│   └── .env.example             # Template
├── railway.json                 # Monorepo config
└── MISSION_ANSWERS.md           # This report
```

**Requirements:**
-  All code runs without errors
-  Multi-stage Dockerfile (image < 500 MB)
-  API key authentication
-  Rate limiting (10 req/min)
-  Cost guard ($10/month)
-  Health + readiness checks
-  Graceful shutdown
-  Stateless design (Redis)
-  No hardcoded secrets

---

### 3. Service Domain Link

- [x] Public URL and DEPLOYMENT.md created.

Create a file `DEPLOYMENT.md` with your deployed service information:

```markdown
# Deployment Information

## Public URL
https://day12ha-tang-cloudvadeployment-production-22ec.up.railway.app

## Platform
Railway

## Test Commands

### Health Check
```bash
curl https://day12ha-tang-cloudvadeployment-production-22ec.up.railway.app/health
# Expected: {"status": "ok"}
```

### API Test (with authentication)
```bash
curl -X POST https://day12ha-tang-cloudvadeployment-production-22ec.up.railway.app/chat \
  -H "X-API-Key: travel-secret-123" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

## Environment Variables Set
- PORT: 8080
- REDIS_URL: (Managed by Railway)
- AGENT_API_KEY: travel-secret-123
- OPENROUTER_API_KEY: sk-or-...
```

##  Pre-Submission Checklist

- [x] Repository is public (or instructor has access)
- [x] `MISSION_ANSWERS.md` completed with all exercises
- [x] `DEPLOYMENT.md` has working public URL
- [x] All source code in `06-final-project-travelbuddy/` directory
- [x] `README.md` has clear setup instructions
- [x] No `.env` file committed (only `.env.example`)
- [x] No hardcoded secrets in code
- [x] Public URL is accessible and working
- [x] Screenshots included in `screenshots/` folder
- [x] Repository has clear commit history

---

##  Self-Test

Before submitting, verify your deployment:

```bash
# 1. Health check
curl https://your-app.railway.app/health

# 2. Authentication required
curl https://your-app.railway.app/ask
# Should return 401

# 3. With API key works
curl -H "X-API-Key: YOUR_KEY" https://your-app.railway.app/ask \
  -X POST -d '{"user_id":"test","question":"Hello"}'
# Should return 200

# 4. Rate limiting
for i in {1..15}; do 
  curl -H "X-API-Key: YOUR_KEY" https://your-app.railway.app/ask \
    -X POST -d '{"user_id":"test","question":"test"}'; 
done
# Should eventually return 429
```

---

##  Submission

**Submit your GitHub repository URL:**

```
https://github.com/your-username/day12-agent-deployment
```

**Deadline:** 17/4/2026

---

##  Quick Tips

1.  Test your public URL from a different device
2.  Make sure repository is public or instructor has access
3.  Include screenshots of working deployment
4.  Write clear commit messages
5.  Test all commands in DEPLOYMENT.md work
6.  No secrets in code or commit history

---

##  Need Help?

- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Review [CODE_LAB.md](CODE_LAB.md)
- Ask in office hours
- Post in discussion forum

---

**Good luck! **
