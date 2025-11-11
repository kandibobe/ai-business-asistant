# 🤝 Contributing to AI Business Assistant

Thank you for your interest in contributing to the AI Business Assistant project! This guide will help you get started with contributing code, documentation, or other improvements.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Documentation](#documentation)
- [Community](#community)

---

## 📜 Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors. Please be professional, constructive, and kind in all interactions.

**Expected Behavior:**
- Use welcoming and inclusive language
- Respect differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

**Unacceptable Behavior:**
- Harassment, discrimination, or offensive comments
- Trolling or insulting/derogatory comments
- Publishing others' private information
- Any conduct which would be inappropriate in a professional setting

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **PostgreSQL 14+**
- **Redis 7+**
- **Docker & Docker Compose** (recommended)
- **Git**

### Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/ai-business-asistant.git
cd ai-business-asistant

# Add upstream remote
git remote add upstream https://github.com/kandibobe/ai-business-asistant.git
```

### Set Up Development Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install black isort flake8 mypy pytest pytest-cov pre-commit

# Set up pre-commit hooks
pre-commit install

# Copy environment file
cp .env.example .env
# Edit .env with your configuration
```

### Start Development Services

```bash
# Start PostgreSQL and Redis
docker-compose up -d postgres redis

# Run database migrations
alembic upgrade head

# Run tests to verify setup
pytest
```

---

## 🔄 Development Workflow

### 1. Create a Branch

Always create a new branch for your work:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

**Branch Naming Convention:**
- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation changes
- `refactor/description` - Code refactoring
- `test/description` - Test additions/fixes
- `chore/description` - Maintenance tasks

### 2. Make Changes

Write clean, well-documented code following our [Coding Standards](#coding-standards).

### 3. Test Your Changes

```bash
# Run all tests
pytest

# Run specific test types
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# Run with coverage
pytest --cov=. --cov-report=html

# Check code quality
black .
isort .
flake8 .
mypy .
```

### 4. Commit Your Changes

Write clear, descriptive commit messages following [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Good commit messages
git commit -m "feat: add document export to PDF feature"
git commit -m "fix: resolve rate limiter Redis connection issue"
git commit -m "docs: update API documentation"
git commit -m "test: add unit tests for validators"

# Commit message format
<type>: <description>

[optional body]

[optional footer]
```

**Commit Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation only
- `style` - Code style changes (formatting, etc.)
- `refactor` - Code refactoring
- `test` - Adding/updating tests
- `chore` - Maintenance tasks
- `perf` - Performance improvements
- `ci` - CI/CD changes

### 5. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

---

## 📏 Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

- **Line length:** 100 characters (not 79)
- **Formatter:** Black (automatic)
- **Import sorting:** isort with black profile
- **Type hints:** Required for all public functions
- **Docstrings:** Google style

### Code Formatting

```bash
# Format code automatically
black .
isort .

# Or let pre-commit hooks do it automatically
git commit
```

### Type Hints

All public functions and methods must have type hints:

```python
from typing import List, Optional, Dict, Any

def process_document(
    document_id: int,
    user_id: int,
    options: Optional[Dict[str, Any]] = None
) -> Dict[str, str]:
    """
    Process a document for a specific user.

    Args:
        document_id: The ID of the document to process
        user_id: The ID of the user requesting processing
        options: Optional processing options

    Returns:
        Dictionary containing processing results

    Raises:
        DocumentNotFoundError: If document doesn't exist
        ProcessingError: If processing fails
    """
    ...
```

### Docstrings

Use **Google style** docstrings:

```python
def calculate_metrics(data: List[float], threshold: float) -> Dict[str, float]:
    """
    Calculate statistical metrics from data.

    This function computes mean, median, and standard deviation
    for the provided data, filtering values above threshold.

    Args:
        data: List of numeric values to analyze
        threshold: Maximum value to include in calculations

    Returns:
        Dictionary with keys 'mean', 'median', 'std'

    Raises:
        ValueError: If data is empty or threshold is negative

    Example:
        >>> data = [1.0, 2.0, 3.0, 4.0, 5.0]
        >>> metrics = calculate_metrics(data, threshold=4.0)
        >>> print(metrics['mean'])
        2.0
    """
    ...
```

### Error Handling

Use custom exceptions from `utils/error_handlers.py`:

```python
from utils.error_handlers import ValidationError, NotFoundError

def get_document(document_id: int) -> Document:
    """Get document by ID."""
    if document_id < 0:
        raise ValidationError("Document ID must be positive")

    document = db.query(Document).get(document_id)
    if not document:
        raise NotFoundError(f"Document {document_id} not found")

    return document
```

---

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── unit/           # Fast, isolated unit tests
├── integration/    # Tests with DB, Redis, etc.
└── e2e/           # End-to-end workflow tests
```

### Writing Tests

```python
import pytest
from unittest.mock import Mock, patch

@pytest.mark.unit
def test_validate_file_size():
    """Test file size validation."""
    from utils.validators import validate_file_size

    # Test valid file
    assert validate_file_size(1024 * 1024) is True  # 1 MB

    # Test invalid file
    with pytest.raises(ValidationError):
        validate_file_size(100 * 1024 * 1024)  # 100 MB


@pytest.mark.integration
@pytest.mark.asyncio
async def test_document_processing(db_session):
    """Test document processing integration."""
    from tasks import process_pdf_task
    from database.models import Document

    # Setup
    document = Document(filename="test.pdf", status="pending")
    db_session.add(document)
    db_session.commit()

    # Execute
    with patch('tasks.extract_pdf_text', return_value="Test content"):
        result = process_pdf_task(document.id)

    # Verify
    assert result is not None
    db_session.refresh(document)
    assert document.status == "completed"
```

### Test Coverage

- **Minimum coverage:** 70%
- **Target coverage:** 80%+
- Run coverage reports:

```bash
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

---

## 🔀 Pull Request Process

### Before Submitting

✅ **Checklist:**
- [ ] Code follows style guidelines (black, isort, flake8, mypy pass)
- [ ] All tests pass (`pytest`)
- [ ] New tests added for new features
- [ ] Documentation updated (if applicable)
- [ ] Commit messages follow conventions
- [ ] Branch is up to date with main
- [ ] Pre-commit hooks pass

### PR Title Format

Use the same format as commit messages:

```
feat: add document export to PDF
fix: resolve rate limiter issue
docs: update API documentation
```

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Fixes #123
Related to #456

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. **Automated checks** must pass (CI/CD pipeline)
2. **Code review** by at least one maintainer
3. **Address feedback** and update PR
4. **Approval** from maintainer
5. **Merge** (squash and merge preferred)

---

## 🐛 Issue Guidelines

### Before Creating an Issue

- Check if issue already exists
- Search closed issues too
- Try latest version

### Bug Reports

Use the bug report template:

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment**
- OS: [e.g. Ubuntu 22.04]
- Python version: [e.g. 3.10.5]
- Bot version: [e.g. 2.0.0]

**Logs**
```
Paste relevant logs here
```

**Screenshots**
Add screenshots if applicable.
```

### Feature Requests

```markdown
**Feature Description**
Clear description of the feature.

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should this work?

**Alternatives**
Other solutions you've considered.

**Additional Context**
Any other relevant information.
```

---

## 📖 Documentation

### Types of Documentation

- **Code comments** - For complex logic
- **Docstrings** - For all public functions/classes
- **README.md** - Project overview and quick start
- **ARCHITECTURE.md** - System design and architecture
- **API docs** - API endpoint documentation
- **Tutorials** - How-to guides

### Documentation Style

- Use clear, concise language
- Include code examples
- Add diagrams where helpful
- Keep it up to date
- Use proper Markdown formatting

---

## 🌍 Community

### Getting Help

- **Issues:** For bugs and feature requests
- **Discussions:** For questions and general discussion
- **Discord/Telegram:** For real-time chat (if available)

### Recognition

Contributors will be:
- Listed in `CONTRIBUTORS.md`
- Credited in release notes
- Thanked in project README

---

## 🎯 Development Tips

### Useful Commands

```bash
# Run bot in development mode
python main.py

# Run Celery worker
celery -A celery_app worker --loglevel=info

# Run API server
python run_api.py

# Check code quality
make lint  # or run black, isort, flake8, mypy manually

# Run specific tests
pytest tests/unit/test_validators.py::test_validate_email

# Debug mode
python -m pdb main.py
```

### Common Gotchas

- Always activate virtual environment
- Run migrations after pulling changes
- Clear Redis cache if behavior seems strange
- Check `.env` file configuration
- Restart Celery worker after code changes

---

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!

**Questions?** Open an issue or reach out to maintainers.

**Happy coding! 🚀**
