# AI Business Assistant - REST API Documentation

## Overview

REST API для веб-приложения AI Business Intelligence Agent. Построен на FastAPI с поддержкой JWT аутентификации, WebSocket для real-time чата, и полной интеграцией с базой данных PostgreSQL.

## Features

- ✅ JWT Authentication (access + refresh tokens)
- ✅ Document upload and management
- ✅ AI Chat with Gemini API
- ✅ WebSocket real-time chat
- ✅ Analytics and statistics
- ✅ User settings management
- ✅ File validation and security
- ✅ Error handling and logging
- ✅ CORS configured
- ✅ OpenAPI/Swagger documentation

## Installation

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Redis (optional, for caching)

### Install Dependencies

```bash
pip install fastapi uvicorn python-jose passlib bcrypt python-multipart google-generativeai
```

### Environment Variables

Create a `.env` file:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ai_business_assistant

# JWT
JWT_SECRET=your-secret-key-change-in-production

# Gemini API
GEMINI_API_KEY=your-gemini-api-key

# Redis (optional)
REDIS_URL=redis://localhost:6379
```

## Running the API

### Development Mode

```bash
# Option 1: Using uvicorn directly
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Option 2: Using Python
python api/main.py
```

### Production Mode

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## API Endpoints

### Authentication

#### POST `/api/auth/register`
Register a new user

**Request:**
```json
{
  "username": "testuser",
  "password": "securepass123",
  "email": "test@example.com",
  "first_name": "Test",
  "last_name": "User"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "user_id": 1000000,
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User",
    "language": "en",
    "is_premium": false,
    "created_at": "2025-11-10T..."
  },
  "tokens": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer"
  }
}
```

#### POST `/api/auth/login`
Login user

**Request:**
```json
{
  "username": "testuser",
  "password": "securepass123"
}
```

#### GET `/api/auth/me`
Get current user (requires authentication)

**Headers:**
```
Authorization: Bearer <access_token>
```

#### POST `/api/auth/refresh`
Refresh access token (requires refresh token)

---

### Documents

#### GET `/api/documents?page=1&page_size=20`
Get user's documents (paginated)

**Response:**
```json
{
  "documents": [
    {
      "id": 1,
      "file_name": "report.pdf",
      "document_type": "pdf",
      "file_size": 524288,
      "status": "processed",
      "is_active": true,
      "uploaded_at": "2025-11-10T...",
      "processed_at": "2025-11-10T...",
      "summary": "Document summary...",
      "page_count": 10,
      "word_count": 5000
    }
  ],
  "total": 5,
  "page": 1,
  "page_size": 20
}
```

#### POST `/api/documents/upload`
Upload a new document

**Request:** `multipart/form-data`
- file: File (PDF, Excel, Word, Audio, etc.)

**Response:**
```json
{
  "id": 1,
  "file_name": "report.pdf",
  "document_type": "pdf",
  "file_size": 524288,
  "status": "pending",
  "message": "Document uploaded successfully. Processing will start shortly."
}
```

#### GET `/api/documents/{document_id}`
Get document details

#### DELETE `/api/documents/{document_id}`
Delete a document

#### PUT `/api/documents/{document_id}/activate`
Set document as active for chat context

---

### Chat

#### POST `/api/chat/message`
Send a message to AI

**Request:**
```json
{
  "message": "What are the key insights from my document?",
  "document_id": 1
}
```

**Response:**
```json
{
  "answer": "Based on the document, here are the key insights...",
  "response_time": 1.23,
  "timestamp": "2025-11-10T...",
  "question_id": 42
}
```

#### GET `/api/chat/history?document_id=1&limit=50`
Get chat history

**Response:**
```json
{
  "history": [
    {
      "id": 42,
      "question": "What are the key insights?",
      "answer": "Based on the document...",
      "timestamp": "2025-11-10T...",
      "response_time": 1.23,
      "document_id": 1
    }
  ],
  "total": 10
}
```

#### DELETE `/api/chat/history?document_id=1`
Clear chat history

#### WebSocket `/api/chat/ws`
Real-time chat via WebSocket

**Send:**
```json
{
  "message": "Your question here",
  "document_id": 1,
  "user_id": 1000000
}
```

**Receive:**
```json
{
  "answer": "AI response",
  "response_time": 1.23,
  "timestamp": "2025-11-10T..."
}
```

---

### Analytics

#### GET `/api/analytics/stats`
Get user statistics

**Response:**
```json
{
  "total_documents": 5,
  "total_questions": 150,
  "average_response_time": 1.45,
  "documents_by_type": {
    "pdf": 3,
    "excel": 2
  },
  "active_document": {
    "id": 1,
    "file_name": "report.pdf",
    "document_type": "pdf"
  },
  "user_since": "2025-11-01T..."
}
```

#### GET `/api/analytics/dashboard`
Get dashboard statistics (today's activity + charts)

#### GET `/api/analytics/documents/{document_id}/stats`
Get statistics for specific document

---

### Settings

#### GET `/api/settings`
Get user settings

**Response:**
```json
{
  "language": "en",
  "ai_role": "assistant",
  "ai_style": "professional",
  "mode": "standard",
  "notifications_enabled": true
}
```

#### PUT `/api/settings`
Update user settings

**Request:**
```json
{
  "language": "ru",
  "ai_role": "analyst",
  "notifications_enabled": true
}
```

#### POST `/api/settings/language?language=ru`
Quick language change

---

## Authentication

All protected endpoints require JWT authentication.

### Getting a Token

1. Register or login to get access_token
2. Include token in Authorization header:

```bash
curl -H "Authorization: Bearer <access_token>" \
     http://localhost:8000/api/auth/me
```

### Token Expiration

- **Access Token**: 1 hour
- **Refresh Token**: 7 days

### Refreshing Token

```bash
curl -X POST http://localhost:8000/api/auth/refresh \
     -H "Authorization: Bearer <refresh_token>"
```

---

## File Upload Limits

- **Max file size**: 50MB
- **Supported formats**:
  - PDF (.pdf)
  - Excel (.xlsx, .xls, .csv)
  - Word (.docx, .doc)
  - Audio (.mp3, .wav, .m4a, .ogg)
  - Text (.txt)
  - Images (.jpg, .png, .gif, .webp)

---

## Error Handling

All errors return consistent JSON format:

```json
{
  "detail": "Error message",
  "type": "ValueError",
  "path": "/api/chat/message"
}
```

### Common HTTP Status Codes

- **200 OK**: Success
- **201 Created**: Resource created
- **204 No Content**: Success with no body
- **400 Bad Request**: Invalid input
- **401 Unauthorized**: Missing or invalid token
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

---

## Testing the API

### Using cURL

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"Test123!","email":"test@test.com"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"Test123!"}'

# Get current user
curl -H "Authorization: Bearer <token>" \
     http://localhost:8000/api/auth/me

# Upload document
curl -X POST http://localhost:8000/api/documents/upload \
  -H "Authorization: Bearer <token>" \
  -F "file=@document.pdf"

# Send chat message
curl -X POST http://localhost:8000/api/chat/message \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"message":"What is this document about?"}'
```

### Using Python

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# Register
response = requests.post(f"{BASE_URL}/api/auth/register", json={
    "username": "test",
    "password": "Test123!",
    "email": "test@test.com"
})
tokens = response.json()["tokens"]
access_token = tokens["access_token"]

# Get user info
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
user = response.json()
print(user)

# Upload document
files = {"file": open("document.pdf", "rb")}
response = requests.post(
    f"{BASE_URL}/api/documents/upload",
    headers=headers,
    files=files
)
print(response.json())

# Send chat message
response = requests.post(
    f"{BASE_URL}/api/chat/message",
    headers=headers,
    json={"message": "What is this document about?"}
)
print(response.json())
```

---

## WebSocket Chat Example

### JavaScript

```javascript
const ws = new WebSocket('ws://localhost:8000/api/chat/ws')

ws.onopen = () => {
  console.log('Connected to chat')

  // Send message
  ws.send(JSON.stringify({
    message: 'Hello AI!',
    user_id: 1000000
  }))
}

ws.onmessage = (event) => {
  const data = JSON.parse(event.data)
  console.log('AI:', data.answer)
  console.log('Response time:', data.response_time, 's')
}

ws.onerror = (error) => {
  console.error('WebSocket error:', error)
}

ws.onclose = () => {
  console.log('Disconnected from chat')
}
```

---

## Deployment

### Docker

Create `Dockerfile.api`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t ai-assistant-api -f Dockerfile.api .
docker run -p 8000:8000 --env-file .env ai-assistant-api
```

### Production Checklist

- [ ] Change JWT_SECRET to a strong random value
- [ ] Use HTTPS only
- [ ] Enable rate limiting
- [ ] Set up proper logging
- [ ] Configure CORS for your domain
- [ ] Set up monitoring (Sentry, etc.)
- [ ] Use a process manager (systemd, supervisor)
- [ ] Set up SSL certificates
- [ ] Configure firewall rules

---

## Troubleshooting

### Port Already in Use

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Database Connection Error

Check DATABASE_URL in .env file and ensure PostgreSQL is running.

### CORS Error from Frontend

Update `origins` list in `api/main.py`:

```python
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://yourdomain.com"
]
```

---

## License

MIT

## Support

For issues and questions, please create an issue on GitHub.
