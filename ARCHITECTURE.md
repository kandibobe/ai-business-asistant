# 🏗️ Architecture Documentation

AI Business Assistant - Technical Architecture and Design Decisions

**Version:** 2.0.0
**Last Updated:** 2025-11-11
**Status:** Production-Ready

---

## 📋 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Component Details](#component-details)
- [Data Flow](#data-flow)
- [Security Architecture](#security-architecture)
- [Scalability](#scalability)
- [Deployment Architecture](#deployment-architecture)
- [Design Decisions](#design-decisions)
- [Future Improvements](#future-improvements)

---

## 🎯 Overview

AI Business Assistant is a **production-ready Telegram bot** that provides AI-powered document analysis and business intelligence capabilities. The system is built with modern Python technologies and follows microservices principles for scalability and maintainability.

### Core Capabilities

- 📄 **Multi-format Document Processing** (PDF, Excel, Word, Audio)
- 🤖 **AI-Powered Analysis** (Google Gemini)
- 💬 **Natural Language Queries** via Telegram
- 🌐 **REST API** for external integrations
- 📊 **Web Dashboard** for document management
- 🔒 **Enterprise-grade Security** and monitoring

---

## 🏛️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│  Telegram App  │  Web Browser  │  Mobile App  │  API Clients   │
└────────┬────────────────┬────────────────┬────────────┬─────────┘
         │                │                │            │
         ▼                ▼                ▼            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  Telegram Bot API  │  FastAPI REST API  │  WebSocket Gateway   │
│  - Webhook Mode    │  - JWT Auth        │  - Real-time Updates │
│  - Long Polling    │  - Rate Limiting   │                      │
└────────┬────────────────┬─────────────────────────────┬─────────┘
         │                │                             │
         ▼                ▼                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────┐  ┌───────────────┐  ┌──────────────────┐   │
│  │   Handlers    │  │   Services    │  │   Middleware     │   │
│  ├───────────────┤  ├───────────────┤  ├──────────────────┤   │
│  │ - Documents   │  │ - AI Service  │  │ - Auth           │   │
│  │ - Messages    │  │ - File Proc.  │  │ - Rate Limiter   │   │
│  │ - Commands    │  │ - Analytics   │  │ - Error Handler  │   │
│  │ - Callbacks   │  │ - Export      │  │ - Logging        │   │
│  └───────────────┘  └───────────────┘  └──────────────────┘   │
│                                                                  │
└────────┬──────────────────────────────────────────────┬─────────┘
         │                                              │
         ▼                                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PROCESSING LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│                    Celery Workers                                │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────┐ │
│  │ PDF Worker │  │Excel Worker│  │Audio Worker│  │AI Worker │ │
│  └────────────┘  └────────────┘  └────────────┘  └──────────┘ │
│                                                                  │
│  Features:                                                       │
│  - Async task processing                                        │
│  - Retry logic with exponential backoff                         │
│  - Task prioritization                                          │
│  - Result caching                                               │
└────────┬──────────────────────────────────────────────┬─────────┘
         │                                              │
         ▼                                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DATA LAYER                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐        ┌──────────────────┐              │
│  │   PostgreSQL     │        │      Redis       │              │
│  ├──────────────────┤        ├──────────────────┤              │
│  │ - Users          │        │ - Cache          │              │
│  │ - Documents      │        │ - Task Queue     │              │
│  │ - Conversations  │        │ - Rate Limits    │              │
│  │ - Analytics      │        │ - Sessions       │              │
│  └──────────────────┘        └──────────────────┘              │
│                                                                  │
└────────┬──────────────────────────────────────────────┬─────────┘
         │                                              │
         ▼                                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                               │
├─────────────────────────────────────────────────────────────────┤
│  Google Gemini  │  OpenAI Whisper  │  Telegram API  │  Sentry  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                  MONITORING & OBSERVABILITY                      │
├─────────────────────────────────────────────────────────────────┤
│  Prometheus  │  Grafana  │  Sentry  │  ELK Stack  │  Health    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Core Technologies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|----------|
| **Language** | Python | 3.10+ | Main programming language |
| **Bot Framework** | python-telegram-bot | 21.1+ | Telegram bot interface |
| **AI Engine** | Google Gemini | 1.5-pro | Document analysis & NLU |
| **Web Framework** | FastAPI | 0.109+ | REST API server |
| **Task Queue** | Celery | 5.4+ | Async task processing |
| **Message Broker** | Redis | 7.0+ | Cache & task queue |
| **Database** | PostgreSQL | 14+ | Primary data store |
| **ORM** | SQLAlchemy | 2.0+ | Database abstraction |
| **Migrations** | Alembic | 1.13+ | Database versioning |

### Supporting Technologies

| Component | Technology | Purpose |
|-----------|-----------|----------|
| **Validation** | Pydantic | Data validation & settings |
| **Logging** | structlog | Structured logging |
| **Monitoring** | Prometheus | Metrics collection |
| **Visualization** | Grafana | Metrics dashboards |
| **Error Tracking** | Sentry | Error monitoring |
| **Testing** | pytest | Test framework |
| **Code Quality** | black, isort, flake8, mypy | Linting & formatting |
| **Containerization** | Docker | Application packaging |
| **Orchestration** | Docker Compose / Kubernetes | Container management |
| **CI/CD** | GitHub Actions | Automation pipeline |

---

## 🧩 Component Details

### 1. Telegram Bot Layer

**File:** `main.py`

```python
# Handles all Telegram interactions
- Webhook mode (production)
- Long polling mode (development)
- Command handlers (/start, /mydocs, /clear)
- Message handlers (text, documents, audio)
- Callback query handlers (inline buttons)
```

**Key Features:**
- Automatic retry on network errors
- Graceful error handling
- User context tracking
- Multi-language support (i18n)

### 2. API Layer

**Directory:** `api/`

```python
api/
├── routes/          # REST endpoints
│   ├── auth.py      # Authentication
│   ├── documents.py # Document management
│   ├── users.py     # User management
│   └── analytics.py # Analytics data
├── models/          # Pydantic schemas
├── middleware/      # Auth, CORS, rate limiting
└── __init__.py      # FastAPI app initialization
```

**Endpoints:**
- `POST /api/v1/auth/login` - User authentication
- `GET /api/v1/documents` - List user documents
- `POST /api/v1/documents/{id}/query` - Query document
- `GET /api/v1/analytics` - User analytics

### 3. Document Processing Pipeline

**File:** `tasks.py`

```
Document Upload → Validation → Storage → Processing → AI Analysis → Storage → Response
     ↓              ↓            ↓          ↓            ↓             ↓         ↓
  Telegram      File Size    S3/Local   Celery      Gemini API    PostgreSQL  User
               MIME Type                Worker
               Security
```

**Processing Steps:**

1. **Validation**
   - File size check
   - MIME type validation
   - Security scanning
   - Format verification

2. **Extraction**
   - PDF: PyMuPDF (fitz)
   - Excel: pandas, openpyxl
   - Word: python-docx
   - Audio: OpenAI Whisper

3. **Processing**
   - Text normalization
   - Chunking for large documents
   - Metadata extraction
   - Thumbnail generation (images)

4. **AI Analysis**
   - Context preparation
   - Gemini API call
   - Response parsing
   - Result caching

### 4. Database Schema

**File:** `database/models.py`

```sql
users
  ├── id (PK)
  ├── telegram_id (unique)
  ├── username
  ├── tier (free/premium/enterprise)
  ├── status (active/inactive/banned)
  ├── created_at
  └── updated_at

documents
  ├── id (PK)
  ├── user_id (FK → users)
  ├── filename
  ├── file_path
  ├── file_type
  ├── file_size
  ├── text_content (extracted text)
  ├── status (pending/processing/completed/failed)
  ├── created_at
  └── updated_at

conversations
  ├── id (PK)
  ├── user_id (FK → users)
  ├── document_id (FK → documents)
  ├── query (user question)
  ├── response (AI answer)
  ├── tokens_used
  ├── response_time
  └── created_at

analytics
  ├── id (PK)
  ├── user_id (FK → users)
  ├── event_type
  ├── event_data (jsonb)
  ├── created_at
```

### 5. Caching Strategy

**File:** `utils/cache.py`

```python
Cache Layers:
1. L1: In-Memory Cache (local, fast, limited)
2. L2: Redis Cache (distributed, persistent)

Cache Keys:
- ai:response:{doc_id}:{query_hash} → AI responses (TTL: 1 hour)
- doc:text:{doc_id} → Document text (TTL: 7 days)
- user:session:{user_id} → User session (TTL: 24 hours)
- ratelimit:{user_id} → Rate limit counters (TTL: dynamic)
```

### 6. Security Layers

**File:** `utils/security.py`

```
Input → Sanitization → Validation → Authentication → Authorization → Rate Limiting → Processing
  ↓          ↓            ↓              ↓               ↓                ↓             ↓
XSS       SQL Inj.    File Type        JWT          User Tier        Redis        Business
Filter    Detection   Validation       Token        Permissions      Counter       Logic
```

**Security Features:**
- Input sanitization (XSS, SQL injection)
- File validation (size, type, content)
- JWT authentication (API)
- Role-based access control (RBAC)
- Rate limiting (per user/tier)
- HTTPS/TLS encryption
- Secrets management (environment variables)

---

## 🔄 Data Flow

### Document Upload Flow

```
User uploads document via Telegram
         ↓
Handler receives document
         ↓
Validate file (size, type, security)
         ↓
Download file from Telegram servers
         ↓
Save to local storage / S3
         ↓
Create DB record (status: pending)
         ↓
Queue Celery task (process_document_task)
         ↓
Send "Processing..." message to user
         ↓
[CELERY WORKER]
         ↓
Extract text from document
         ↓
Store extracted text in DB
         ↓
Update status to "completed"
         ↓
Send "Ready!" message to user
```

### AI Query Flow

```
User sends text question
         ↓
Handler receives message
         ↓
Check rate limit
         ↓
Find user's active document
         ↓
Check cache for similar query
         ├─ Cache Hit → Return cached response
         └─ Cache Miss ↓
                Queue AI task (query_document_task)
                       ↓
                Send "Thinking..." message
                       ↓
                [CELERY WORKER]
                       ↓
                Prepare context (document + query)
                       ↓
                Call Gemini API
                       ↓
                Parse response
                       ↓
                Cache result
                       ↓
                Store in conversations table
                       ↓
                Send response to user
```

---

## 🔒 Security Architecture

### Authentication & Authorization

```
API Request
     ↓
JWT Token Validation
     ├─ Invalid/Expired → 401 Unauthorized
     └─ Valid ↓
            Extract User ID
                 ↓
            Check User Status
                 ├─ Banned → 403 Forbidden
                 └─ Active ↓
                         Check Permissions
                              ├─ Insufficient → 403 Forbidden
                              └─ OK → Process Request
```

### Rate Limiting Strategy

```python
Rate Limiting Tiers:

Free Tier:
- 10 requests/minute
- 100 requests/hour
- 500 requests/day
- Max 10 documents

Premium Tier:
- 30 requests/minute
- 500 requests/hour
- 5000 requests/day
- Max 100 documents

Enterprise Tier:
- Unlimited requests
- Unlimited documents
- Priority processing
```

### Data Protection

- **Encryption at Rest:** PostgreSQL TDE, encrypted backups
- **Encryption in Transit:** TLS 1.3 for all connections
- **Secret Management:** Environment variables, never in code
- **Access Control:** Row-level security (RLS) in PostgreSQL
- **Audit Logging:** All sensitive operations logged
- **Data Retention:** Automatic cleanup of old data

---

## 📈 Scalability

### Horizontal Scaling

```
Load Balancer
     ├─ Bot Instance 1 ┐
     ├─ Bot Instance 2 ├─ Shared PostgreSQL (primary + replicas)
     ├─ Bot Instance 3 ┘
     │
     ├─ Celery Worker 1 ┐
     ├─ Celery Worker 2 ├─ Shared Redis (cluster mode)
     ├─ Celery Worker 3 ┘
     │
     ├─ API Instance 1 ┐
     ├─ API Instance 2 ├─ Stateless (JWT tokens)
     └─ API Instance 3 ┘
```

### Performance Optimizations

1. **Database:**
   - Connection pooling
   - Query optimization (indexes)
   - Read replicas for analytics
   - Partitioning for large tables

2. **Caching:**
   - Multi-layer cache (L1 + L2)
   - Cache warming strategies
   - Smart invalidation

3. **Async Processing:**
   - Celery for heavy tasks
   - Task prioritization
   - Worker auto-scaling

4. **API:**
   - Response compression (gzip)
   - CDN for static assets
   - GraphQL for flexible queries (future)

### Capacity Planning

| Metric | Current | Target | Limit |
|--------|---------|--------|-------|
| Concurrent Users | 100 | 1,000 | 10,000 |
| Requests/sec | 10 | 100 | 1,000 |
| Documents | 10K | 100K | 1M |
| DB Size | 1 GB | 10 GB | 100 GB |

---

## 🚀 Deployment Architecture

### Production Deployment (Google Cloud Run)

```
Internet
    ↓
Cloud Load Balancer (HTTPS)
    ↓
Cloud Run (Bot + API)
    ├─ Auto-scaling (0-10 instances)
    ├─ Environment: production
    └─ Health checks enabled
    ↓
Cloud SQL (PostgreSQL)
    ├─ High availability
    ├─ Automated backups
    └─ Point-in-time recovery
    ↓
Cloud Memorystore (Redis)
    ├─ Standard tier
    └─ 5 GB memory

External Services:
- Google Gemini API
- OpenAI API
- Telegram Bot API
- Sentry (error tracking)
```

### Kubernetes Deployment (Alternative)

```yaml
# Deployment manifest
kind: Deployment
metadata:
  name: ai-bot
spec:
  replicas: 3
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    spec:
      containers:
      - name: bot
        image: gcr.io/project/ai-bot:latest
        resources:
          requests:
            cpu: 100m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
```

---

## 🎨 Design Decisions

### Why Celery for Task Processing?

**Pros:**
- ✅ Mature, battle-tested
- ✅ Great Python integration
- ✅ Flexible routing
- ✅ Built-in retry logic
- ✅ Monitoring tools (Flower)

**Alternatives Considered:**
- ❌ RQ (Redis Queue) - Less feature-rich
- ❌ Dramatiq - Smaller community
- ✅ **Celery** - Best overall choice

### Why PostgreSQL over MongoDB?

**Decision:** PostgreSQL with JSONB

**Reasons:**
- Structured data (users, documents)
- ACID compliance required
- Complex queries and joins
- JSONB for flexible metadata
- Better ecosystem for analytics

### Why Gemini over GPT-4?

**Decision:** Google Gemini 1.5 Pro

**Reasons:**
- Larger context window (up to 1M tokens)
- Better pricing for long documents
- Native PDF/image understanding
- Strong multilingual support (Russian)
- Competitive quality

**Fallback:** OpenAI GPT-4 (configurable)

---

## 🔮 Future Improvements

### Short Term (v2.1)

- [ ] GraphQL API endpoint
- [ ] WebSocket support for real-time updates
- [ ] Document versioning
- [ ] Collaborative document sharing
- [ ] Advanced analytics dashboard

### Medium Term (v2.5)

- [ ] Multi-tenant support (organizations)
- [ ] Custom AI model fine-tuning
- [ ] Voice message processing (Telegram voice notes)
- [ ] OCR for scanned documents
- [ ] Integration marketplace (Zapier, n8n)

### Long Term (v3.0)

- [ ] Self-hosted LLM option (Llama, Mistral)
- [ ] Federated learning for privacy
- [ ] Blockchain-based document verification
- [ ] Mobile apps (iOS, Android)
- [ ] Desktop apps (Electron)

---

## 📚 References

### Related Documentation

- [README.md](README.md) - Project overview
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment instructions
- [SECURITY.md](SECURITY.md) - Security policies
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues

### External Resources

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Google Gemini API](https://ai.google.dev/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

---

**Last Updated:** 2025-11-11
**Maintainer:** AI Business Assistant Team
**Questions?** Open an issue on GitHub
