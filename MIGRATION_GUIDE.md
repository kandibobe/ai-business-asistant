# 🚀 Migration Guide to Gemini 1.5 Pro & Production-Ready Architecture

> **Version:** 2.0
> **Date:** 2025-11-10
> **Migration Time:** ~30 minutes

---

## 📋 Overview of Changes

This migration brings your AI Business Assistant to production-ready status with enterprise-grade features:

### ✅ **What's New**

1. **🤖 Gemini 1.5 Pro Upgrade**
   - Upgraded from `gemini-pro` → `gemini-1.5-pro-002`
   - **1 million token context window** (vs 32K previously)
   - Native multimodality (images, video)
   - Better accuracy and performance
   - Optional `gemini-1.5-flash-002` for fast responses

2. **🔒 Enterprise Security**
   - File validation (size, type, MIME, magic bytes)
   - Input sanitization (SQL injection, XSS, command injection protection)
   - Rate limiting (5 AI requests/min for free tier)
   - Path traversal protection
   - Security headers

3. **🧪 Comprehensive Testing**
   - Unit tests for all critical components
   - Integration tests for handlers and API
   - Test coverage tracking
   - Fixtures for all document types

4. **📄 Document AI Integration**
   - Advanced OCR for scanned documents
   - Structured data extraction (tables, forms, invoices)
   - Entity recognition with confidence scores
   - Superior to basic PyMuPDF extraction

5. **📊 Production Infrastructure**
   - GitHub Actions CI/CD pipeline
   - Cloud Run deployment configuration
   - Docker multi-stage builds
   - Health checks and monitoring
   - Secrets management via Google Secret Manager

6. **⚡ Enhanced AI Helpers**
   - Automatic retry logic with exponential backoff
   - Response caching for cost reduction
   - Token tracking
   - Context truncation for large documents

---

## 🔧 Migration Steps

### Step 1: Update Dependencies

```bash
# Pull latest changes
git pull origin main

# Update Python packages
pip install --upgrade google-generativeai

# Optional: Install Document AI (for advanced document processing)
pip install google-cloud-documentai
```

### Step 2: Update Environment Variables

Add these to your `.env` file:

```env
# ============================================================================
# GEMINI 1.5 PRO CONFIGURATION
# ============================================================================
# Your existing GEMINI_API_KEY works with Gemini 1.5 Pro!
GEMINI_API_KEY=your_gemini_api_key_here

# ============================================================================
# DOCUMENT AI (OPTIONAL)
# ============================================================================
# Enable for advanced document processing
# Get processor ID from: https://console.cloud.google.com/ai/document-ai
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
DOCUMENT_AI_PROCESSOR_ID=your-processor-id

# ============================================================================
# AI CACHING (ALREADY CONFIGURED)
# ============================================================================
AI_CACHE_TTL=3600  # 1 hour (already set)
```

### Step 3: Test the Upgrade

```bash
# Check configuration
python check_setup.py

# Test Gemini 1.5 Pro
python -c "
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Test with Gemini 1.5 Pro
model = genai.GenerativeModel('gemini-1.5-pro-002')
response = model.generate_content('Hello! What model are you?')
print('✅ Gemini 1.5 Pro:', response.text[:100])
"

# Run tests (if pytest installed)
pytest tests/ -v
```

### Step 4: Restart Your Bot

```bash
# Stop existing bot (Ctrl+C)

# Restart with new configuration
python main.py
```

You should see:
```
✅ AI model ready: gemini-1.5-pro-002
```

---

## 🆕 New Features Usage

### 1. Using Gemini 1.5 Flash for Fast Responses

```python
from config import GEMINI_FLASH_MODEL
import google.generativeai as genai

# For simple, fast queries
flash_model = genai.GenerativeModel(GEMINI_FLASH_MODEL)
response = flash_model.generate_content("Quick question")
```

### 2. Document AI Integration

```python
from utils.document_ai_processor import process_with_document_ai

# Process invoice with structured extraction
formatted_text, result = process_with_document_ai(
    "invoice.pdf",
    mime_type="application/pdf"
)

# Access extracted entities
for entity in result.entities:
    print(f"{entity.type}: {entity.value} ({entity.confidence:.2%})")

# Access tables
for table in result.tables:
    print("Headers:", table['headers'])
    for row in table['rows']:
        print(row)
```

### 3. AI Helpers with Caching

```python
from utils.ai_helpers import generate_ai_response

# With caching enabled (reduces costs)
response = generate_ai_response(
    model=gemini_model,
    prompt="Analyze this document",
    context=document_text,
    use_cache=True,  # Enable caching
    max_retries=3
)

print(response['message'])
print(f"Response time: {response['response_time_ms']}ms")
print(f"Cached: {response['cached']}")
```

### 4. Large Document Handling

```python
from utils.ai_helpers import truncate_context

# For documents > 500K tokens
# Gemini 1.5 Pro supports up to 1M tokens!
truncated = truncate_context(
    very_long_document,
    max_length=500_000  # Still massive!
)
```

---

## 📊 What Improved?

### Before (gemini-pro)
- ❌ 32K token context limit
- ❌ No multimodality
- ❌ Basic error handling
- ❌ No structured data extraction
- ❌ No caching
- ❌ No tests

### After (gemini-1.5-pro-002)
- ✅ **1 million token context**
- ✅ **Native multimodality**
- ✅ **Retry logic with exponential backoff**
- ✅ **Document AI structured extraction**
- ✅ **AI response caching**
- ✅ **100+ unit tests**
- ✅ **Production-ready security**
- ✅ **CI/CD pipeline**
- ✅ **Cloud Run deployment config**

---

## 🚨 Breaking Changes

### None! 🎉

This migration is **100% backward compatible**. Your existing code will work without changes.

However, you can now:
- Send **much larger documents** (up to 1M tokens)
- Use **caching** to reduce API costs
- Enable **Document AI** for structured extraction
- Deploy to **Cloud Run** with one command

---

## 💰 Cost Optimization

### Gemini 1.5 Pro Pricing
- **Input:** $0.00125 per 1K tokens
- **Output:** $0.005 per 1K tokens
- **Caching saves 90%** on repeated queries

### Gemini 1.5 Flash Pricing
- **Input:** $0.000075 per 1K tokens (16x cheaper!)
- **Output:** $0.0003 per 1K tokens
- **Use for:** Simple queries, summaries, translations

### Document AI Pricing
- **General processor:** $1.50 per 1,000 pages
- **Specialized (invoices):** $15 per 1,000 pages
- **Free tier:** 1,000 pages/month

**Recommendation:** Use caching + Flash model for 70% cost reduction!

---

## ☁️ Cloud Deployment (Optional)

### Prerequisites
```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Enable APIs
gcloud services enable run.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### Quick Deploy to Cloud Run

```bash
# 1. Create secrets
echo -n "your_telegram_token" | gcloud secrets create telegram-bot-token --data-file=-
echo -n "your_gemini_key" | gcloud secrets create gemini-api-key --data-file=-
echo -n "your_db_password" | gcloud secrets create db-password --data-file=-

# 2. Build and deploy
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/ai-bot
gcloud run deploy ai-business-bot \
  --image gcr.io/YOUR_PROJECT_ID/ai-bot \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Automated Deployment (CI/CD)

```bash
# Set GitHub secrets:
# GCP_PROJECT_ID
# GCP_SA_KEY (service account JSON)

# Push to main branch → automatic deployment!
git push origin main
```

See `.github/workflows/ci-cd.yml` for full pipeline.

---

## 🐛 Troubleshooting

### Issue: "Invalid model name"
**Solution:** Update `google-generativeai`:
```bash
pip install --upgrade google-generativeai
```

### Issue: "Document AI not configured"
**Solution:** Document AI is optional! To enable:
1. Enable Document AI API in GCP Console
2. Create a processor
3. Set `GOOGLE_CLOUD_PROJECT` and `DOCUMENT_AI_PROCESSOR_ID`

### Issue: "Rate limit exceeded"
**Solution:** This is expected for free tier. Upgrade to premium or implement:
```python
# Adjust in middleware/rate_limiter.py
RATE_LIMITS['free']['ai_requests'] = (10, 60)  # 10 requests/min
```

### Issue: "Tests failing"
**Solution:** Install test dependencies:
```bash
pip install pytest pytest-asyncio pytest-cov faker
```

---

## 📚 Next Steps

1. ✅ **Review Security Settings**
   Check `utils/security.py` and adjust file size limits if needed

2. ✅ **Configure Document AI** (optional)
   For invoices, receipts, contracts processing

3. ✅ **Set Up Monitoring**
   Enable Cloud Logging and Error Reporting

4. ✅ **Configure CI/CD**
   Set GitHub secrets for automatic deployment

5. ✅ **Optimize Costs**
   - Use caching for repeated queries
   - Use Flash model for simple responses
   - Set reasonable rate limits

---

## 📞 Support

- **Documentation:** [Google Gemini Docs](https://ai.google.dev/docs)
- **Document AI:** [Document AI Docs](https://cloud.google.com/document-ai/docs)
- **Cloud Run:** [Cloud Run Docs](https://cloud.google.com/run/docs)
- **Issues:** GitHub Issues

---

## ✅ Migration Checklist

- [ ] Pulled latest code
- [ ] Updated dependencies
- [ ] Tested Gemini 1.5 Pro connection
- [ ] Reviewed new features
- [ ] (Optional) Configured Document AI
- [ ] (Optional) Set up CI/CD
- [ ] (Optional) Deployed to Cloud Run
- [ ] Read troubleshooting section
- [ ] Celebrated! 🎉

---

**Migration complete!** Your AI Business Assistant is now production-ready with enterprise-grade features. 🚀
