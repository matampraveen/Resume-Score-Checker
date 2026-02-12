# AI-Powered Resume Screening System - Deployment & Production Readiness

## 1. Environment Setup (Production)
For a production-grade deployment, we move away from `runserver` to a robust WSGI/ASGI server.

### 1.1 Core Components
-   **Web Server**: Nginx (Reverse Proxy, SSL termination, Static file serving).
-   **App Server**: Gunicorn (WSGI) or Uvicorn (ASGI).
-   **Database**: MongoDB Atlas (Managed Service) or a Replica Set on dedicated VMs.
-   **Process Control**: Systemd or Supervisor (if not using Docker).

### 1.2 Environment Variables (`.env`)
Never commit sensitive keys. Use a `.env` file:
```bash
DJANGO_SECRET_KEY=prod_key_...
DEBUG=False
MONGO_URI=mongodb+srv://user:pass@cluster...
ALLOWED_HOSTS=hr-portal.company.com
```

## 2. Docker & Containerization
We use a multi-stage Docker build for smaller image sizes.

### 2.1 `Dockerfile`
```dockerfile
# Stage 1: Build
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Run
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "resume_screener.wsgi:application"]
```

### 2.2 `docker-compose.prod.yml`
```yaml
version: '3.8'
services:
  web:
    build: .
    env_file: .env
    ports: ["8000:8000"]
    depends_on:
      - mongo
  nginx:
    image: nginx:alpine
    ports: ["80:80", "443:443"]
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
```

## 3. CI/CD Pipeline (GitHub Actions)
Automate testing and deployment.

### 3.1 Workflow (`.github/workflows/deploy.yml`)
1.  **Trigger**: Push to `main`.
2.  **Test**: Run `pytest` and `flake8`.
3.  **Build**: Build Docker image and push to ECR/Docker Hub.
4.  **Deploy**: SSH into EC2 instance, pull new image, and `docker-compose up -d`.

## 4. Logging & Monitoring
-   **Application Logs**: Use `logging` module to write to stdout. Docker captures this.
-   **Centralized Logging**: ELK Stack (Elasticsearch, Logstash, Kibana) or Datadog.
-   **Error Tracking**: Sentry integration for real-time alerting on 500 errors.
-   **Metrics**: Prometheus + Grafana to monitor request latency and ML inference time.

## 5. Security Best Practices
-   **SSL/TLS**: Enforce HTTPS via Let's Encrypt (Certbot).
-   **Headers**: Use `django-csp` and `SECURE_SSL_REDIRECT = True`.
-   **Rate Limiting**: Use Nginx or DRF throttling (`AnonRateThrottle`) to prevent DDoS.
-   **Input Validation**: Strict validation on File Uploads (check mimetypes, restrict file size to 5MB).

## 6. Performance Optimization
-   **Caching**: Redis for caching frequent API responses (e.g., Job Lists).
-   **Async Processing**: Use Celery + Redis to offload Resume Parsing and ML Screening.
    -   *Current*: Synchronous (OK for demo).
    -   *Prod*: User uploads -> Task Queued -> Worker processes -> Notification sent.
-   **Database**: Indexes on `job_id` and `score` are critical.

## 7. Scaling Strategy
-   **Horizontal Scaling**: Run multiple Gunicorn workers (`2 * CPU + 1`).
-   **Load Balancing**: Use an AWS ALB or Nginx to distribute traffic across ECS tasks or Autoscaling Groups.
-   **Database Scaling**: MongoDB Sharding if resume volume exceeds 1TB.
