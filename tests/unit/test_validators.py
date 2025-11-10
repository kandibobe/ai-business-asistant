"""
Unit tests for Pydantic validators.
Tests request/response validation schemas.
"""
import pytest
from pydantic import ValidationError
from utils.validators import (
    UserRegister,
    UserLogin,
    ChatMessage,
    UserSettings,
    SettingsUpdate,
    QRCodeRequest,
    HashGenerateRequest,
)


@pytest.mark.unit
class TestUserRegisterValidator:
    """Tests for UserRegister schema."""

    def test_valid_registration(self):
        """Test valid user registration data."""
        data = {
            'email': 'test@example.com',
            'username': 'test_user123',
            'password': 'SecurePass123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        user = UserRegister(**data)
        assert user.email == data['email']
        assert user.username == data['username']
        assert user.password == data['password']

    def test_username_too_short(self):
        """Test username minimum length validation."""
        data = {
            'email': 'test@example.com',
            'username': 'ab',  # Too short (min 3)
            'password': 'SecurePass123'
        }
        with pytest.raises(ValidationError) as exc_info:
            UserRegister(**data)
        assert 'username' in str(exc_info.value).lower()

    def test_username_special_characters(self):
        """Test username allows underscores and dashes."""
        data = {
            'email': 'test@example.com',
            'username': 'test_user-123',
            'password': 'SecurePass123'
        }
        user = UserRegister(**data)
        assert user.username == 'test_user-123'

    def test_username_invalid_characters(self):
        """Test username rejects invalid characters."""
        data = {
            'email': 'test@example.com',
            'username': 'test user!',  # Space and ! not allowed
            'password': 'SecurePass123'
        }
        with pytest.raises(ValidationError):
            UserRegister(**data)

    def test_password_too_short(self):
        """Test password minimum length."""
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'Short1'  # Too short (min 8)
        }
        with pytest.raises(ValidationError):
            UserRegister(**data)

    def test_password_no_uppercase(self):
        """Test password requires uppercase letter."""
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'nouppercase123'
        }
        with pytest.raises(ValidationError) as exc_info:
            UserRegister(**data)
        assert 'uppercase' in str(exc_info.value).lower()

    def test_password_no_lowercase(self):
        """Test password requires lowercase letter."""
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'NOLOWERCASE123'
        }
        with pytest.raises(ValidationError) as exc_info:
            UserRegister(**data)
        assert 'lowercase' in str(exc_info.value).lower()

    def test_password_no_digit(self):
        """Test password requires digit."""
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'NoDigitPass'
        }
        with pytest.raises(ValidationError) as exc_info:
            UserRegister(**data)
        assert 'digit' in str(exc_info.value).lower()

    def test_invalid_email(self):
        """Test email validation."""
        data = {
            'email': 'not_an_email',
            'username': 'testuser',
            'password': 'SecurePass123'
        }
        with pytest.raises(ValidationError) as exc_info:
            UserRegister(**data)
        assert 'email' in str(exc_info.value).lower()

    def test_optional_fields(self):
        """Test that first_name and last_name are optional."""
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'SecurePass123'
        }
        user = UserRegister(**data)
        assert user.first_name is None
        assert user.last_name is None


@pytest.mark.unit
class TestChatMessageValidator:
    """Tests for ChatMessage schema."""

    def test_valid_message(self):
        """Test valid chat message."""
        data = {
            'message': 'What is the summary of this document?',
            'document_id': 123
        }
        msg = ChatMessage(**data)
        assert msg.message == data['message']
        assert msg.document_id == 123

    def test_message_without_document(self):
        """Test message without document_id."""
        data = {'message': 'General question'}
        msg = ChatMessage(**data)
        assert msg.document_id is None

    def test_message_too_short(self):
        """Test message minimum length."""
        data = {'message': ''}
        with pytest.raises(ValidationError):
            ChatMessage(**data)

    def test_message_too_long(self):
        """Test message maximum length."""
        data = {'message': 'a' * 15000}  # Max 10000
        with pytest.raises(ValidationError):
            ChatMessage(**data)

    def test_message_sanitization(self):
        """Test that message is sanitized."""
        data = {'message': '  Multiple   spaces   here  '}
        msg = ChatMessage(**data)
        # Should have stripped and normalized spaces
        assert msg.message.startswith('Multiple')
        assert '   ' not in msg.message

    def test_message_null_bytes_removed(self):
        """Test null bytes are removed."""
        data = {'message': 'Text\x00with\x00nulls'}
        msg = ChatMessage(**data)
        assert '\x00' not in msg.message


@pytest.mark.unit
class TestUserSettingsValidator:
    """Tests for UserSettings schema."""

    def test_valid_settings(self):
        """Test valid user settings."""
        data = {
            'language': 'en',
            'mode': 'advanced',
            'ai_role': 'analyst',
            'response_style': 'detailed'
        }
        settings = UserSettings(**data)
        assert settings.language == 'en'
        assert settings.mode == 'advanced'

    def test_invalid_language(self):
        """Test invalid language code."""
        data = {'language': 'invalid'}
        with pytest.raises(ValidationError):
            UserSettings(**data)

    def test_invalid_mode(self):
        """Test invalid mode."""
        data = {'mode': 'invalid'}
        with pytest.raises(ValidationError):
            UserSettings(**data)

    def test_invalid_ai_role(self):
        """Test invalid AI role."""
        data = {'ai_role': 'invalid_role'}
        with pytest.raises(ValidationError):
            UserSettings(**data)

    def test_invalid_response_style(self):
        """Test invalid response style."""
        data = {'response_style': 'invalid_style'}
        with pytest.raises(ValidationError):
            UserSettings(**data)

    def test_default_values(self):
        """Test default settings values."""
        settings = UserSettings()
        assert settings.language == 'ru'
        assert settings.mode == 'standard'
        assert settings.ai_role == 'assistant'
        assert settings.response_style == 'standard'
        assert settings.notifications_enabled is True
        assert settings.auto_analysis_enabled is False

    def test_boolean_settings(self):
        """Test boolean settings."""
        data = {
            'notifications_enabled': False,
            'auto_analysis_enabled': True
        }
        settings = UserSettings(**data)
        assert settings.notifications_enabled is False
        assert settings.auto_analysis_enabled is True


@pytest.mark.unit
class TestSettingsUpdateValidator:
    """Tests for SettingsUpdate schema."""

    def test_partial_update(self):
        """Test partial settings update."""
        data = {'language': 'en'}
        update = SettingsUpdate(**data)
        assert update.language == 'en'
        assert update.mode is None
        assert update.ai_role is None

    def test_multiple_fields_update(self):
        """Test updating multiple fields."""
        data = {
            'language': 'de',
            'mode': 'fast',
            'notifications_enabled': False
        }
        update = SettingsUpdate(**data)
        assert update.language == 'de'
        assert update.mode == 'fast'
        assert update.notifications_enabled is False

    def test_empty_update(self):
        """Test empty update (all fields None)."""
        update = SettingsUpdate()
        assert all(getattr(update, field) is None for field in ['language', 'mode', 'ai_role'])


@pytest.mark.unit
class TestHashGenerateRequest:
    """Tests for HashGenerateRequest schema."""

    def test_default_algorithm(self):
        """Test default hash algorithm."""
        data = {'text': 'test string'}
        req = HashGenerateRequest(**data)
        assert req.algorithm == 'sha256'

    def test_custom_algorithm(self):
        """Test custom hash algorithm."""
        algorithms = ['md5', 'sha1', 'sha256', 'sha512']
        for algo in algorithms:
            data = {'text': 'test', 'algorithm': algo}
            req = HashGenerateRequest(**data)
            assert req.algorithm == algo

    def test_invalid_algorithm(self):
        """Test invalid hash algorithm."""
        data = {'text': 'test', 'algorithm': 'invalid'}
        with pytest.raises(ValidationError):
            HashGenerateRequest(**data)

    def test_text_max_length(self):
        """Test text maximum length."""
        data = {'text': 'a' * 150000}  # Max 100000
        with pytest.raises(ValidationError):
            HashGenerateRequest(**data)


@pytest.mark.unit
class TestQRCodeRequest:
    """Tests for QRCodeRequest schema."""

    def test_valid_qr_request(self):
        """Test valid QR code request."""
        data = {'text': 'https://example.com', 'size': 500}
        req = QRCodeRequest(**data)
        assert req.text == 'https://example.com'
        assert req.size == 500

    def test_default_size(self):
        """Test default QR code size."""
        data = {'text': 'test'}
        req = QRCodeRequest(**data)
        assert req.size == 300

    def test_size_too_small(self):
        """Test QR code minimum size."""
        data = {'text': 'test', 'size': 50}  # Min 100
        with pytest.raises(ValidationError):
            QRCodeRequest(**data)

    def test_size_too_large(self):
        """Test QR code maximum size."""
        data = {'text': 'test', 'size': 2000}  # Max 1000
        with pytest.raises(ValidationError):
            QRCodeRequest(**data)

    def test_text_too_long(self):
        """Test QR code text maximum length."""
        data = {'text': 'a' * 3000}  # Max 2000
        with pytest.raises(ValidationError):
            QRCodeRequest(**data)
