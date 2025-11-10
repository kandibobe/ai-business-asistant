# 🧪 Test Suite for AI Business Assistant

Comprehensive test suite with unit and integration tests.

---

## 📊 Test Coverage

**Target:** > 70% code coverage

**Current Tests:**
- **Unit Tests:** 100+ tests
- **Integration Tests:** 15+ tests
- **Security Tests:** 40+ tests

---

## 🚀 Quick Start

### Install Test Dependencies

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest
```

### Run with Coverage Report

```bash
pytest --cov=. --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html
```

---

## 📂 Test Structure

```
tests/
├── conftest.py                 # Shared fixtures
├── unit/                       # Unit tests (fast, isolated)
│   ├── test_models.py          # Database models
│   ├── test_crud.py            # CRUD operations
│   ├── test_security.py        # Security & validation
│   ├── test_validators.py      # Pydantic schemas
│   └── test_rate_limiter.py    # Rate limiting
├── integration/                # Integration tests
│   ├── test_document_handlers.py  # Document processing flow
│   └── test_message_handlers.py   # Message handling flow
└── fixtures/                   # Test data files

```

---

## 🏷️ Test Markers

### Run Specific Test Categories

**Unit tests only:**
```bash
pytest -m unit
```

**Integration tests:**
```bash
pytest -m integration
```

**Security tests:**
```bash
pytest -m security
```

**Database tests:**
```bash
pytest -m database
```

**Fast tests (exclude slow):**
```bash
pytest -m "not slow"
```

### Available Markers

- `unit` - Fast, isolated unit tests
- `integration` - Integration tests (uses DB/Redis)
- `slow` - Slow running tests
- `security` - Security-related tests
- `database` - Tests requiring database
- `redis` - Tests requiring Redis
- `telegram` - Telegram bot handler tests
- `api` - REST API endpoint tests

---

## 📋 Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific file
pytest tests/unit/test_models.py

# Run specific test class
pytest tests/unit/test_models.py::TestUserModel

# Run specific test function
pytest tests/unit/test_models.py::TestUserModel::test_create_user

# Run tests matching pattern
pytest -k "test_create"
```

### Coverage Commands

```bash
# HTML coverage report
pytest --cov=. --cov-report=html

# Terminal coverage report
pytest --cov=. --cov-report=term-missing

# XML coverage report (for CI/CD)
pytest --cov=. --cov-report=xml

# Fail if coverage below threshold
pytest --cov=. --cov-fail-under=70
```

### Advanced Options

```bash
# Stop on first failure
pytest -x

# Show local variables in traceback
pytest -l

# Run failed tests from last run
pytest --lf

# Run failed tests first, then others
pytest --ff

# Parallel execution (requires pytest-xdist)
pytest -n auto

# Show slowest tests
pytest --durations=10
```

---

## 🔧 Fixtures

### Available Fixtures

**Database:**
- `db_engine` - SQLite in-memory database
- `db_session` - Database session (auto rollback)
- `sample_user` - Sample user in DB
- `sample_document` - Sample document in DB

**Data:**
- `faker_instance` - Faker for generating test data
- `sample_user_data` - User data dict
- `sample_document_data` - Document data dict

**Files:**
- `temp_directory` - Temporary directory
- `sample_pdf_file` - Sample PDF file
- `sample_excel_file` - Sample Excel file
- `sample_word_file` - Sample Word file
- `sample_audio_file` - Sample audio file

**Mocks:**
- `mock_telegram_update` - Mock Telegram Update
- `mock_telegram_context` - Mock Telegram Context
- `mock_gemini_model` - Mock AI model
- `mock_redis_client` - Mock Redis client

**Environment:**
- `test_env_vars` - Test environment variables

---

## 📝 Writing New Tests

### Unit Test Example

```python
import pytest
from database.models import User

@pytest.mark.unit
@pytest.mark.database
def test_create_user(db_session, sample_user_data):
    """Test creating a new user."""
    user = User(**sample_user_data)
    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    assert user.username == sample_user_data['username']
```

### Integration Test Example

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.integration
@pytest.mark.telegram
@pytest.mark.asyncio
async def test_handle_document(
    mock_telegram_update,
    mock_telegram_context,
    mock_redis_client
):
    """Test document upload handler."""
    # Setup
    mock_telegram_update.message.document.file_name = 'test.pdf'

    # Execute
    with patch('handlers.documents.process_pdf_task') as mock_task:
        await handle_document(mock_telegram_update, mock_telegram_context)

    # Verify
    mock_task.delay.assert_called_once()
```

### Security Test Example

```python
import pytest
from utils.security import sanitize_text_input, SecurityError

@pytest.mark.unit
@pytest.mark.security
def test_sql_injection_detected():
    """Test SQL injection detection."""
    dangerous_input = "'; DROP TABLE users; --"

    with pytest.raises(SecurityError):
        sanitize_text_input(dangerous_input)
```

---

## 🎯 Test Best Practices

### Do's ✅

- Write descriptive test names
- Use fixtures for setup/teardown
- Test edge cases and error conditions
- Mock external dependencies (DB, APIs, Redis)
- Keep tests independent
- Use markers to categorize tests
- Aim for > 70% coverage

### Don'ts ❌

- Don't test external libraries
- Don't write flaky tests
- Don't share state between tests
- Don't hardcode test data
- Don't ignore test failures
- Don't skip testing error paths

---

## 🐛 Debugging Tests

### Show Print Statements

```bash
pytest -s
```

### Debug with PDB

```bash
pytest --pdb
```

Add breakpoint in code:
```python
def test_something():
    import pdb; pdb.set_trace()
    # Your test code
```

### Show Warnings

```bash
pytest -W all
```

### Verbose Output

```bash
pytest -vv
```

---

## 📊 Coverage Reports

### View Coverage

After running tests with coverage:

```bash
# View in browser
open htmlcov/index.html

# View in terminal
pytest --cov=. --cov-report=term
```

### Coverage Configuration

See `.coveragerc` for configuration:
- Excluded files/patterns
- Coverage thresholds
- Report formats

---

## 🔄 Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest --cov=. --cov-report=xml
      - uses: codecov/codecov-action@v3
```

---

## 🚨 Troubleshooting

### Tests Fail to Import Modules

```bash
# Add current directory to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

### Database Tests Fail

Check that fixtures are properly scoped:
```python
@pytest.fixture(scope="function")  # New DB for each test
def db_session(db_engine):
    ...
```

### Redis Tests Fail

Ensure Redis mock is properly injected:
```python
def test_something(mock_redis_client):
    # mock_redis_client is automatically injected
    ...
```

### Async Tests Fail

Make sure to use `@pytest.mark.asyncio`:
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_func()
    assert result is not None
```

---

## 📈 Test Metrics

### Track Test Metrics

```bash
# Count total tests
pytest --collect-only | grep "test session starts"

# Show test durations
pytest --durations=0

# Generate JUnit XML report
pytest --junitxml=report.xml
```

---

## 🎓 Learn More

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [coverage.py](https://coverage.readthedocs.io/)
- [Faker documentation](https://faker.readthedocs.io/)

---

**Last Updated:** 2025-11-09
**Test Framework:** pytest 8.0+
