# 📊 Monitoring & Observability

Complete monitoring setup for AI Business Assistant using Prometheus and Grafana.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Prometheus Setup](#prometheus-setup)
- [Grafana Setup](#grafana-setup)
- [Available Metrics](#available-metrics)
- [Alerting](#alerting)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This monitoring stack provides:
- **Real-time metrics** via Prometheus
- **Visual dashboards** via Grafana
- **Error tracking** via Sentry (optional)
- **Log aggregation** via ELK Stack (optional)

### Architecture

```
Application (Bot + API + Workers)
         ↓
   Prometheus (metrics collection)
         ↓
   Grafana (visualization)
         ↓
   Alertmanager (notifications)
```

---

## 🚀 Quick Start

### Using Docker Compose

```bash
# Start monitoring stack
docker-compose up -d prometheus grafana

# Access Grafana
open http://localhost:3000
# Default login: admin / admin

# Access Prometheus
open http://localhost:9090
```

### Manual Setup

```bash
# 1. Install Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.40.0/prometheus-2.40.0.linux-amd64.tar.gz
tar xvfz prometheus-*.tar.gz
cd prometheus-*

# 2. Copy configuration
cp monitoring/prometheus.yml .

# 3. Start Prometheus
./prometheus --config.file=prometheus.yml

# 4. Install Grafana
# See: https://grafana.com/docs/grafana/latest/setup-grafana/installation/

# 5. Import dashboard
# In Grafana UI: Import → Upload JSON → monitoring/grafana_dashboard.json
```

---

## 📈 Prometheus Setup

### Configuration File

Create `prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  # Bot + API metrics
  - job_name: 'ai-bot'
    static_configs:
      - targets: ['localhost:8000']
        labels:
          service: 'api'
      - targets: ['localhost:8001']
        labels:
          service: 'bot'

  # Celery worker metrics
  - job_name: 'celery'
    static_configs:
      - targets: ['localhost:9091']

  # PostgreSQL metrics (optional)
  - job_name: 'postgres'
    static_configs:
      - targets: ['localhost:9187']

  # Redis metrics (optional)
  - job_name: 'redis'
    static_configs:
      - targets: ['localhost:9121']
```

### Adding Metrics Endpoint

The application exposes metrics at `/metrics` (configured in `main.py` and `run_api.py`).

```python
# Already configured in the application
from prometheus_client import make_asgi_app
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
```

---

## 📊 Grafana Setup

### Import Dashboard

1. Open Grafana: `http://localhost:3000`
2. Login (default: admin/admin)
3. Go to **Dashboards** → **Import**
4. Upload `monitoring/grafana_dashboard.json`
5. Select Prometheus datasource
6. Click **Import**

### Dashboard Overview

**Available Panels:**

1. **Request Rate** - HTTP requests per second
2. **Response Time (p95)** - 95th percentile latency
3. **HTTP Status Codes** - 2xx, 4xx, 5xx distribution
4. **Error Rate** - 5xx errors per second
5. **Celery Tasks** - Task count by status
6. **Celery Task Duration** - Average task execution time
7. **AI Service Metrics** - AI requests and cache hits
8. **AI Cache Hit Rate** - Cache efficiency percentage
9. **Documents Processed** - Documents by type
10. **Active Users** - Current active user count

### Creating Alerts

In Grafana dashboard:

1. Edit any panel
2. Go to **Alert** tab
3. Create alert rule:
   ```
   WHEN avg() OF query(A, 5m, now) IS ABOVE 0.1
   ```
4. Set notification channel (Slack, Email, PagerDuty, etc.)

---

## 📏 Available Metrics

### HTTP Metrics

Exposed by FastAPI and Bot:

```prometheus
# Total HTTP requests
http_requests_total{method="GET", endpoint="/api/v1/documents", status="200"}

# Request duration histogram
http_request_duration_seconds_bucket{method="POST", endpoint="/api/v1/auth/login", le="0.1"}

# Requests in progress
http_requests_in_progress{method="GET", endpoint="/health"}
```

### Celery Metrics

Task processing metrics:

```prometheus
# Total tasks
celery_task_total{task="process_pdf_task", status="success"}

# Task runtime
celery_task_runtime_seconds{task="process_pdf_task"}

# Task queue length
celery_queue_length{queue="default"}

# Workers active
celery_workers_active
```

### AI Service Metrics

AI and caching metrics:

```prometheus
# AI requests
ai_requests_total{model="gemini-1.5-pro"}

# Cache hits/misses
ai_cache_hits_total
ai_cache_misses_total

# AI response time
ai_response_time_seconds{model="gemini-1.5-pro"}
```

### Document Processing Metrics

```prometheus
# Documents processed
documents_processed_total{document_type="pdf", status="success"}

# Processing time
document_processing_time_seconds{document_type="excel"}

# File size histogram
document_size_bytes_bucket{document_type="pdf", le="1000000"}
```

### User Metrics

```prometheus
# Active users
active_users_total

# New registrations
user_registrations_total

# User tier distribution
users_by_tier{tier="premium"}
```

### System Metrics (optional)

Using `psutil` integration:

```prometheus
# CPU usage
process_cpu_usage_percent

# Memory usage
process_memory_usage_bytes

# Open file descriptors
process_open_fds
```

---

## 🔔 Alerting

### Prometheus Alerting Rules

Create `alerts.yml`:

```yaml
groups:
  - name: ai_bot_alerts
    interval: 30s
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors/sec"

      # High response time
      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1.0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High response time"
          description: "P95 latency is {{ $value }}s"

      # Celery queue backlog
      - alert: CeleryQueueBacklog
        expr: celery_queue_length > 100
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Celery queue backlog"
          description: "{{ $value }} tasks in queue"

      # Low cache hit rate
      - alert: LowCacheHitRate
        expr: (ai_cache_hits_total / (ai_cache_hits_total + ai_cache_misses_total)) < 0.5
        for: 15m
        labels:
          severity: info
        annotations:
          summary: "Low AI cache hit rate"
          description: "Cache hit rate is {{ $value }}%"

      # Database connection issues
      - alert: DatabaseConnectionFailed
        expr: database_health_check == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Database connection failed"
          description: "Cannot connect to PostgreSQL"

      # Redis connection issues
      - alert: RedisConnectionFailed
        expr: redis_health_check == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Redis connection failed"
          description: "Cannot connect to Redis"
```

### Alertmanager Configuration

Create `alertmanager.yml`:

```yaml
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname', 'severity']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'default'
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty'
    - match:
        severity: warning
      receiver: 'slack'

receivers:
  - name: 'default'
    email_configs:
      - to: 'alerts@yourcompany.com'

  - name: 'slack'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'
        channel: '#alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: 'YOUR_PAGERDUTY_KEY'
```

---

## 🛠️ Troubleshooting

### Metrics Not Appearing

**Check Prometheus targets:**
```bash
# Open Prometheus UI
open http://localhost:9090/targets

# Should see all targets as "UP"
```

**Verify metrics endpoint:**
```bash
# Check if metrics are exposed
curl http://localhost:8000/metrics

# Should see Prometheus format metrics
```

**Check application logs:**
```bash
# Look for metrics-related errors
docker logs ai-bot | grep metrics
```

### Grafana Dashboard Empty

**Check Prometheus datasource:**
1. Grafana → Configuration → Data Sources
2. Test Prometheus connection
3. Should show "Data source is working"

**Verify query:**
```promql
# Run in Prometheus UI to test
rate(http_requests_total[5m])
```

**Check time range:**
- Dashboard time range may be too far in past
- Change to "Last 5 minutes"

### High Memory Usage

Prometheus retains data in memory. Configure retention:

```yaml
# prometheus.yml
global:
  storage.tsdb.retention.time: 15d
  storage.tsdb.retention.size: 10GB
```

---

## 📚 Additional Resources

### Documentation
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Python Client](https://github.com/prometheus/client_python)

### Pre-built Dashboards
- [Grafana Dashboard Library](https://grafana.com/grafana/dashboards/)
- [FastAPI Dashboard](https://grafana.com/grafana/dashboards/16110)
- [PostgreSQL Dashboard](https://grafana.com/grafana/dashboards/9628)

### Tutorials
- [Prometheus Getting Started](https://prometheus.io/docs/prometheus/latest/getting_started/)
- [Grafana Fundamentals](https://grafana.com/tutorials/grafana-fundamentals/)

---

## 🤝 Contributing

To add new metrics:

1. Use `utils/metrics.py` helper functions
2. Instrument code with Prometheus client
3. Update this documentation
4. Add to Grafana dashboard

Example:
```python
from utils.metrics import track_request_duration

@track_request_duration
async def my_handler():
    # Your code here
    pass
```

---

**Last Updated:** 2025-11-11
**Maintainer:** AI Business Assistant Team
