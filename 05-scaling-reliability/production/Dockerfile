# Scaling Demo Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Cài đặt dependencies
COPY 05-scaling-reliability/develop/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install redis  # Cần cho stateless mode

# Copy source code
COPY 05-scaling-reliability/production/app.py .
COPY utils/ /app/utils/

ENV PYTHONPATH=/app
ENV PORT=8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
