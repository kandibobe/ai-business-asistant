# 🚀 Production Deployment Guide

Complete guide for deploying AI Business Assistant to production.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Infrastructure Setup](#infrastructure-setup)
3. [Application Deployment](#application-deployment)
4. [Security Checklist](#security-checklist)
5. [Monitoring & Maintenance](#monitoring--maintenance)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Services

- **Python 3.10+**
- **PostgreSQL 14+** - Main database
- **Redis 7+** - Caching and rate limiting
- **Docker** (recommended) - Container orchestration

### API Keys

Obtain these API keys before deployment:

1. **Telegram Bot Token** - From [@BotFather](https://t.me/botfather)
2. **Google Gemini API Key** - From [Google AI Studio](https://makersuite.google.com/)
3. **OpenAI API Key** (optional) - From [OpenAI Platform](https://platform.openai.com/)

---

## Infrastructure Setup

### Option 1: Docker Compose (Recommended)

**1. Start infrastructure:**

```bash
docker-compose up -d
```

This starts:
- PostgreSQL (port 5432)
- Redis (port 6379)

**2. Verify services:**

```bash
docker-compose ps
```

### Option 2: Manual Installation

#### PostgreSQL

```bash
# Install PostgreSQL
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE ai_bot_db;
CREATE USER ai_bot_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE ai_bot_db TO ai_bot_user;
\q
```

#### Redis

```bash
# Install Redis
sudo apt-get install redis-server

# Start Redis
sudo systemctl start redis
sudo systemctl enable redis

# Verify
redis-cli ping  # Should return: PONG
```

---

## Application Deployment

### Step 1: Clone and Configure

```bash
# Clone repository
git clone https://github.com/yourusername/ai-business-asistant.git
cd ai-business-asistant

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with production values
nano .env
```

**Critical environment variables:**

```bash
# Telegram
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Google Gemini AI
GEMINI_API_KEY=your_gemini_api_key_here

# OpenAI (optional)
OPENAI_API_KEY=your_openai_api_key_here

# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=ai_bot_user
DB_PASS=your_secure_password_here
DB_NAME=ai_bot_db

# Redis
REDIS_URL=redis://localhost:6379/0

# API Configuration
API_PORT=8000
JWT_SECRET_KEY=$(openssl rand -hex 32)  # Generate secure key!
ALLOWED_ORIGINS=https://yourdomain.com

# Logging
LOG_LEVEL=INFO
JSON_LOGS=true
LOG_FILE=/var/log/ai-bot/app.log

# Caching
AI_CACHE_TTL=3600
```

### Step 3: Database Migrations

```bash
# Run initial migration
python migrate.py upgrade

# Verify
python migrate.py current
```

### Step 4: Test Configuration

```bash
# Test Telegram bot
python main.py

# In another terminal, test REST API
cd api
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Step 5: Setup Celery Worker

```bash
# Start Celery worker
celery -A celery_app worker --loglevel=info --concurrency=4

# Or use systemd service (see below)
```

---

## Production Setup with Systemd

### 1. Telegram Bot Service

Create `/etc/systemd/system/ai-bot.service`:

```ini
[Unit]
Description=AI Business Assistant Telegram Bot
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/ai-business-asistant
Environment="PATH=/path/to/ai-business-asistant/.venv/bin"
ExecStart=/path/to/ai-business-asistant/.venv/bin/python main.py
Restart=always
RestartSec=10

# Logging
StandardOutput=append:/var/log/ai-bot/bot.log
StandardError=append:/var/log/ai-bot/bot-error.log

[Install]
WantedBy=multi-user.target
```

### 2. FastAPI Service

Create `/etc/systemd/system/ai-api.service`:

```ini
[Unit]
Description=AI Business Assistant REST API
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/ai-business-asistant
Environment="PATH=/path/to/ai-business-asistant/.venv/bin"
ExecStart=/path/to/ai-business-asistant/.venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

# Logging
StandardOutput=append:/var/log/ai-bot/api.log
StandardError=append:/var/log/ai-bot/api-error.log

[Install]
WantedBy=multi-user.target
```

### 3. Celery Worker Service

Create `/etc/systemd/system/ai-celery.service`:

```ini
[Unit]
Description=AI Business Assistant Celery Worker
After=network.target redis.service

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/ai-business-asistant
Environment="PATH=/path/to/ai-business-asistant/.venv/bin"
ExecStart=/path/to/ai-business-asistant/.venv/bin/celery -A celery_app worker --loglevel=info --concurrency=4
Restart=always
RestartSec=10

# Logging
StandardOutput=append:/var/log/ai-bot/celery.log
StandardError=append:/var/log/ai-bot/celery-error.log

[Install]
WantedBy=multi-user.target
```

### 4. Enable and Start Services

```bash
# Create log directory
sudo mkdir -p /var/log/ai-bot
sudo chown your_user:your_user /var/log/ai-bot

# Reload systemd
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable ai-bot.service
sudo systemctl enable ai-api.service
sudo systemctl enable ai-celery.service

# Start services
sudo systemctl start ai-bot.service
sudo systemctl start ai-api.service
sudo systemctl start ai-celery.service

# Check status
sudo systemctl status ai-bot.service
sudo systemctl status ai-api.service
sudo systemctl status ai-celery.service
```

---

## Web Application Deployment

### Build React Frontend

```bash
cd web-app

# Install dependencies
npm install

# Build for production
npm run build

# Output will be in web-app/dist/
```

### Nginx Configuration

Create `/etc/nginx/sites-available/ai-bot`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL Configuration (use certbot for Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # React app (static files)
    location / {
        root /path/to/ai-business-asistant/web-app/dist;
        try_files $uri $uri/ /index.html;

        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # API proxy
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # API docs (optional - disable in production for security)
    location /api/docs {
        proxy_pass http://localhost:8000/api/docs;
        proxy_set_header Host $host;

        # Basic auth for docs
        auth_basic "API Documentation";
        auth_basic_user_file /etc/nginx/.htpasswd;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/ai-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL Certificate (Let's Encrypt)

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal is configured automatically
```

---

## Security Checklist

### ✅ Before Going Live

- [ ] Change all default passwords
- [ ] Generate secure JWT_SECRET_KEY (`openssl rand -hex 32`)
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Configure firewall (UFW or iptables)
- [ ] Set LOG_LEVEL=INFO or WARNING (not DEBUG)
- [ ] Enable JSON_LOGS=true for log aggregation
- [ ] Rotate API keys regularly
- [ ] Backup .env file securely (not in Git!)
- [ ] Configure database backups
- [ ] Set up monitoring and alerts
- [ ] Review and limit ALLOWED_ORIGINS
- [ ] Disable API docs in production or add auth
- [ ] Configure rate limiting thresholds
- [ ] Review file upload size limits

### Firewall Configuration

```bash
# Allow SSH, HTTP, HTTPS
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Block direct access to database and Redis from outside
sudo ufw deny 5432/tcp
sudo ufw deny 6379/tcp

# Enable firewall
sudo ufw enable
```

---

## Monitoring & Maintenance

### Health Checks

```bash
# Check bot status
curl http://localhost:8000/api/health

# Check Redis
redis-cli ping

# Check PostgreSQL
psql -U ai_bot_user -d ai_bot_db -c "SELECT 1;"

# Check services
sudo systemctl status ai-bot ai-api ai-celery
```

### Log Monitoring

```bash
# View live logs
sudo journalctl -u ai-bot.service -f
sudo journalctl -u ai-api.service -f
sudo journalctl -u ai-celery.service -f

# View recent errors
sudo journalctl -u ai-bot.service --since "1 hour ago" --priority=err

# Application logs
tail -f /var/log/ai-bot/bot.log
tail -f /var/log/ai-bot/api.log
```

### Database Backup

```bash
# Manual backup
pg_dump -U ai_bot_user ai_bot_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Automated daily backups (add to crontab)
0 2 * * * /usr/bin/pg_dump -U ai_bot_user ai_bot_db | gzip > /backups/ai_bot_$(date +\%Y\%m\%d).sql.gz
```

### Cache Statistics

```bash
# View cache stats
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/chat/cache/stats

# Clear cache if needed
curl -X DELETE -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/chat/cache/clear
```

### Performance Monitoring

Add to `.env`:

```bash
SENTRY_DSN=your_sentry_dsn_here  # For error tracking
```

---

## Troubleshooting

### Bot Not Starting

```bash
# Check logs
sudo journalctl -u ai-bot.service -n 50

# Common issues:
# 1. Invalid bot token
# 2. Database connection failed
# 3. Redis not running
# 4. Missing dependencies
```

### Database Connection Issues

```bash
# Test connection
psql -h localhost -U ai_bot_user -d ai_bot_db

# Check PostgreSQL is running
sudo systemctl status postgresql

# Check credentials in .env
```

### Redis Connection Issues

```bash
# Test Redis
redis-cli ping

# Check Redis is running
sudo systemctl status redis

# Check Redis URL in .env
```

### High Memory Usage

```bash
# Check memory usage
free -h

# Reduce Celery concurrency
# In ai-celery.service, change --concurrency=4 to --concurrency=2

# Clear Redis cache
redis-cli FLUSHDB
```

### API Rate Limiting Issues

If users are getting rate limited too frequently:

1. Adjust limits in `middleware/rate_limiter.py`
2. Upgrade users to premium tier
3. Clear rate limit keys: `redis-cli DEL rate_limit:*`

---

## Updates and Rollbacks

### Deploy New Version

```bash
# 1. Pull latest code
git pull origin main

# 2. Install any new dependencies
source .venv/bin/activate
pip install -r requirements.txt

# 3. Run database migrations
python migrate.py upgrade

# 4. Restart services
sudo systemctl restart ai-bot ai-api ai-celery

# 5. Verify
sudo systemctl status ai-bot ai-api ai-celery
```

### Rollback Procedure

```bash
# 1. Stop services
sudo systemctl stop ai-bot ai-api ai-celery

# 2. Restore database backup
psql -U ai_bot_user ai_bot_db < backup_20250110.sql

# 3. Checkout previous version
git checkout <previous_commit>

# 4. Downgrade database if needed
python migrate.py downgrade

# 5. Restart services
sudo systemctl start ai-bot ai-api ai-celery
```

---

## Cost Optimization

### AI API Costs

- **Enable caching** - Already configured (AI_CACHE_TTL=3600)
- Cache hit rate: ~30-50% reduction in API calls
- Monitor usage in Google Cloud Console
- Set up budget alerts

### Infrastructure Costs

**Small Deployment (< 100 users):**
- VPS: $10-20/month (DigitalOcean, Linode)
- Domain: $10/year
- Total: ~$15/month

**Medium Deployment (100-1000 users):**
- VPS: $40-80/month
- Managed PostgreSQL: $15/month
- Redis Cloud: $10/month
- Total: ~$70/month

---

## Support

### Documentation

- [API Documentation](http://localhost:8000/api/docs)
- [Alembic Migrations](./alembic/README.md)
- [Top 10 Improvements](./TOP_10_IMPROVEMENTS.md)
- [Security Guide](./SECURITY.md)

### Getting Help

- GitHub Issues: [Report bugs](https://github.com/yourusername/ai-business-asistant/issues)
- Check logs first: `sudo journalctl -u ai-bot -n 100`
- Include environment: OS, Python version, error messages

---

## Success Checklist

After deployment, verify:

- [ ] Bot responds to /start command in Telegram
- [ ] Web app loads at https://yourdomain.com
- [ ] Users can login/register
- [ ] File upload works
- [ ] AI chat responds correctly
- [ ] All services are running (systemctl status)
- [ ] Logs are being written
- [ ] Database backups are configured
- [ ] SSL certificate is valid
- [ ] Monitoring is active

---

**🎉 Congratulations! Your AI Business Assistant is now live in production!**
