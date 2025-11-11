# 🤖 AI Business Intelligence Agent

> **Transform your documents into actionable insights with AI-powered analysis**

A production-ready **Telegram Bot** and **Web Application** that uses Google Gemini AI to analyze documents (PDF, Excel, Word), answer questions, and generate business intelligence reports.

---

## 🎯 **For Whom?**

Perfect for:
- 📊 **Business Analysts** - Extract insights from reports and spreadsheets
- 📝 **Content Managers** - Analyze and summarize large documents
- 💼 **Entrepreneurs** - Get quick answers from business documents
- 🎓 **Students & Researchers** - Study materials analysis
- 🏢 **Teams** - Collaborative document intelligence

---

## ✨ **Key Features**

### 📄 **Multi-Format Document Processing**
- **PDF** - Extract text, tables, and analyze content
- **Excel** - Parse spreadsheets, analyze data, generate insights
- **Word** - Process documents and extract information
- **URLs** - Scrape and analyze web pages
- **Audio** - Transcribe meetings and calls (OpenAI Whisper)

### 💬 **Intelligent Q&A**
- Ask questions about uploaded documents in natural language
- Context-aware responses powered by Google Gemini AI
- Multi-turn conversations with document context
- Response caching for faster repeated queries

### 📊 **Analytics & Reporting**
- User activity statistics
- Document usage analytics
- Export reports to PDF
- Visualizations and charts

### 🌐 **Multilingual Support**
- Interface in **Russian**, **English**, and **German**
- Auto-detection of document language
- Localized error messages and help

### 🔐 **Enterprise-Ready Security**
- **JWT authentication** for web app
- **Rate limiting** to prevent abuse
- **Input validation** and sanitization
- **Role-Based Access Control (RBAC)**
- **Secure file handling** with validation

### 💻 **Developer Tools**
Built-in utilities for developers:
- JSON formatter/validator
- Base64 encoder/decoder
- Hash generators (MD5, SHA256, SHA512)
- UUID generator
- Regex tester
- And more...

---

## 🚀 **Quick Demo**

### Telegram Bot
1. Send a PDF document
2. Ask questions: *"What are the main conclusions?"*
3. Get instant AI-powered answers

### Web Application
1. Upload documents via drag-and-drop
2. View document library
3. Chat with your documents
4. Export analysis to PDF

---

## 🛠️ **Tech Stack**

### Backend
- **Python 3.11+** with async/await
- **FastAPI** - Modern REST API
- **PostgreSQL** - Reliable data storage
- **Redis** - High-speed caching
- **Celery** - Background task processing
- **SQLAlchemy** - ORM with migrations
- **Google Gemini AI** - Advanced language model

### Frontend
- **React 18** with TypeScript
- **Vite** - Lightning-fast build tool
- **Material-UI 5** - Professional design
- **React Router v6** - Navigation
- **Axios** - API communication

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **Alembic** - Database migrations
- **pytest** - Comprehensive testing
- **GitHub Actions** - CI/CD ready

---

## 📦 **Installation**

### Prerequisites
- Python 3.11+
- Node.js 18+ (for web app)
- PostgreSQL 14+
- Redis 7+
- Docker & Docker Compose (recommended)

### Quick Start

```bash
# 1. Clone repository
git clone https://github.com/yourusername/ai-business-assistant.git
cd ai-business-assistant

# 2. Set up environment
cp .env.example .env
# Edit .env with your API keys

# 3. Start services with Docker
docker-compose up -d

# 4. Install Python dependencies
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 5. Run database migrations
alembic upgrade head

# 6. Start the bot
python main.py
```

For detailed installation instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 🔑 **Configuration**

Create `.env` file with your credentials:

```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_from_@BotFather

# Google Gemini AI
GEMINI_API_KEY=your_gemini_api_key

# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=ai_bot_user
DB_PASS=secure_password
DB_NAME=ai_bot_db

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT Secret (auto-generated)
JWT_SECRET_KEY=your-secret-key

# Optional: OpenAI (for audio transcription)
OPENAI_API_KEY=your_openai_key
```

---

## 📊 **Architecture**

```
┌─────────────────┐
│  Telegram Bot   │──┐
└─────────────────┘  │
                     ├──▶ ┌──────────────┐      ┌────────────┐
┌─────────────────┐  │    │   FastAPI    │─────▶│ PostgreSQL │
│  Web App (React)│──┘    │   Backend    │      └────────────┘
└─────────────────┘       └──────────────┘
                                 │                ┌────────────┐
                                 ├───────────────▶│   Redis    │
                                 │                └────────────┘
                          ┌──────┴──────┐
                          │   Celery    │
                          │   Workers   │
                          └─────────────┘
                                 │
                          ┌──────┴──────┐
                          │ Google      │
                          │ Gemini AI   │
                          └─────────────┘
```

---

## 🧪 **Testing**

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test category
pytest tests/unit/
pytest tests/integration/
```

**Test Coverage:** 85%+ across core functionality

---

## 📈 **Performance**

- **Response Time:** < 2s for cached queries
- **Document Processing:** ~5-10s per document (depending on size)
- **Concurrent Users:** Tested with 100+ simultaneous users
- **Uptime:** 99.9% with proper infrastructure

---

## 🔒 **Security**

- ✅ Input validation and sanitization
- ✅ SQL injection prevention (parameterized queries)
- ✅ XSS protection
- ✅ Rate limiting (per user/endpoint)
- ✅ Secure file upload validation
- ✅ JWT token authentication
- ✅ HTTPS/TLS support ready
- ✅ Environment variable encryption

See [SECURITY.md](SECURITY.md) for details.

---

## 🌍 **Deployment**

### Docker (Recommended)

```bash
docker-compose up -d
```

### Manual Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guides on:
- Heroku deployment
- AWS EC2 deployment
- DigitalOcean deployment
- Vercel (frontend)
- Railway.app

---

## 🤝 **Contributing**

This is a demonstration project showcasing full-stack development skills.

If you'd like similar functionality for your business:
- 📧 Email: your.email@example.com
- 💼 LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- 🌐 Portfolio: [yourwebsite.com](https://yourwebsite.com)

---

## 📝 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🎓 **Skills Demonstrated**

This project showcases:

### Backend Development
- ✅ RESTful API design (FastAPI)
- ✅ Async programming (asyncio)
- ✅ Database design and ORM (SQLAlchemy)
- ✅ Background task processing (Celery)
- ✅ Caching strategies (Redis)
- ✅ AI integration (Google Gemini)
- ✅ Document processing (PDF, Excel, Word)

### Frontend Development
- ✅ Modern React with hooks
- ✅ TypeScript for type safety
- ✅ Material-UI component library
- ✅ Responsive design
- ✅ State management

### DevOps & Infrastructure
- ✅ Docker containerization
- ✅ Database migrations (Alembic)
- ✅ Environment configuration
- ✅ Logging and monitoring
- ✅ CI/CD ready

### Best Practices
- ✅ Clean code architecture
- ✅ Comprehensive testing
- ✅ Security-first approach
- ✅ Documentation
- ✅ Git workflow

---

## 📞 **Contact for Custom Development**

Need a similar solution for your business? I can build:
- Custom Telegram bots
- AI-powered document analysis systems
- Web applications with modern stack
- API integrations
- Full-stack solutions

**Let's discuss your project!**

---

<div align="center">

**Made with ❤️ by [Your Name]**

[Portfolio](https://yourwebsite.com) • [LinkedIn](https://linkedin.com/in/yourprofile) • [Email](mailto:your.email@example.com)

</div>
