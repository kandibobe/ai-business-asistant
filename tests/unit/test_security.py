"""
Unit tests for security module.
Tests file validation, sanitization, and security checks.
"""
import pytest
import os
from utils.security import (
    validate_file_extension,
    validate_file_size,
    validate_url,
    sanitize_filename,
    sanitize_text_input,
    get_safe_file_path,
    validate_file,
    FileValidationError,
    SecurityError,
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZES,
)


@pytest.mark.unit
@pytest.mark.security
class TestFileExtensionValidation:
    """Tests for file extension validation."""

    def test_valid_pdf_extension(self):
        """Test valid PDF extension."""
        assert validate_file_extension('document.pdf', 'pdf') is True

    def test_valid_excel_extensions(self):
        """Test valid Excel extensions."""
        assert validate_file_extension('spreadsheet.xlsx', 'excel') is True
        assert validate_file_extension('spreadsheet.xls', 'excel') is True

    def test_valid_word_extension(self):
        """Test valid Word extension."""
        assert validate_file_extension('document.docx', 'word') is True

    def test_valid_audio_extensions(self):
        """Test valid audio extensions."""
        assert validate_file_extension('audio.mp3', 'audio') is True
        assert validate_file_extension('audio.wav', 'audio') is True
        assert validate_file_extension('audio.ogg', 'audio') is True

    def test_case_insensitive(self):
        """Test that extension check is case-insensitive."""
        assert validate_file_extension('Document.PDF', 'pdf') is True
        assert validate_file_extension('SPREADSHEET.XLSX', 'excel') is True

    def test_invalid_extension(self):
        """Test invalid extension raises error."""
        with pytest.raises(FileValidationError) as exc_info:
            validate_file_extension('malware.exe', 'pdf')
        assert '.exe' in str(exc_info.value)

    def test_unknown_file_type(self):
        """Test unknown file type raises error."""
        with pytest.raises(FileValidationError) as exc_info:
            validate_file_extension('file.txt', 'unknown_type')
        assert 'Unknown file type' in str(exc_info.value)


@pytest.mark.unit
@pytest.mark.security
class TestFileSizeValidation:
    """Tests for file size validation."""

    def test_valid_file_size(self, sample_pdf_file):
        """Test valid file size."""
        assert validate_file_size(sample_pdf_file, 'pdf') is True

    def test_empty_file(self, temp_directory):
        """Test empty file raises error."""
        empty_file = os.path.join(temp_directory, 'empty.pdf')
        with open(empty_file, 'w') as f:
            pass  # Create empty file

        with pytest.raises(FileValidationError) as exc_info:
            validate_file_size(empty_file, 'pdf')
        assert 'empty' in str(exc_info.value).lower()

    def test_file_too_large(self, temp_directory):
        """Test file exceeding size limit."""
        large_file = os.path.join(temp_directory, 'large.pdf')

        # Create a file larger than PDF limit (50 MB)
        # We'll create a 1MB file and test with a smaller limit
        with open(large_file, 'wb') as f:
            f.write(b'0' * (1024 * 1024))  # 1 MB

        # Temporarily reduce limit for testing
        import utils.security as sec_module
        original_limit = sec_module.MAX_FILE_SIZES['pdf']
        sec_module.MAX_FILE_SIZES['pdf'] = 500 * 1024  # 500 KB

        try:
            with pytest.raises(FileValidationError) as exc_info:
                validate_file_size(large_file, 'pdf')
            assert 'too large' in str(exc_info.value).lower()
        finally:
            # Restore original limit
            sec_module.MAX_FILE_SIZES['pdf'] = original_limit

    def test_nonexistent_file(self):
        """Test nonexistent file raises error."""
        with pytest.raises(FileValidationError) as exc_info:
            validate_file_size('/nonexistent/file.pdf', 'pdf')
        assert 'not found' in str(exc_info.value).lower()


@pytest.mark.unit
@pytest.mark.security
class TestFilenameSanitization:
    """Tests for filename sanitization."""

    def test_safe_filename_unchanged(self):
        """Test that safe filename remains unchanged."""
        safe_name = 'document_123.pdf'
        assert sanitize_filename(safe_name) == safe_name

    def test_path_traversal_removed(self):
        """Test path traversal attempts are removed."""
        dangerous = '../../etc/passwd'
        safe = sanitize_filename(dangerous)
        assert '..' not in safe
        assert '/' not in safe
        assert safe == 'passwd'

    def test_special_characters_replaced(self):
        """Test special characters are replaced."""
        dangerous = 'file<script>alert(1)</script>.pdf'
        safe = sanitize_filename(dangerous)
        assert '<' not in safe
        assert '>' not in safe
        assert 'script' in safe
        assert '.pdf' in safe

    def test_null_bytes_removed(self):
        """Test null bytes are removed."""
        dangerous = 'file\x00name.pdf'
        safe = sanitize_filename(dangerous)
        assert '\x00' not in safe

    def test_long_filename_truncated(self):
        """Test very long filenames are truncated."""
        long_name = 'a' * 300 + '.pdf'
        safe = sanitize_filename(long_name)
        assert len(safe) <= 255
        assert safe.endswith('.pdf')

    def test_unicode_characters(self):
        """Test unicode characters are replaced."""
        unicode_name = 'документ_тест.pdf'
        safe = sanitize_filename(unicode_name)
        # Cyrillic should be replaced with underscores
        assert all(c.isalnum() or c in '._-' for c in safe)


@pytest.mark.unit
@pytest.mark.security
class TestTextInputSanitization:
    """Tests for text input sanitization."""

    def test_safe_text_unchanged(self):
        """Test safe text remains unchanged."""
        safe_text = 'This is a normal question about the document.'
        assert sanitize_text_input(safe_text) == safe_text

    def test_sql_injection_detected(self):
        """Test SQL injection patterns are detected."""
        sql_patterns = [
            "'; DROP TABLE users; --",
            "1' UNION SELECT * FROM users--",
            "admin'--",
            "1' OR '1'='1",
        ]

        for pattern in sql_patterns:
            with pytest.raises(SecurityError) as exc_info:
                sanitize_text_input(pattern)
            assert 'SQL' in str(exc_info.value) or 'dangerous' in str(exc_info.value).lower()

    def test_command_injection_detected(self):
        """Test command injection patterns are detected."""
        command_patterns = [
            "test && rm -rf /",
            "test || cat /etc/passwd",
            "test; whoami",
            "test$(malicious)",
            "test`malicious`",
        ]

        for pattern in command_patterns:
            with pytest.raises(SecurityError) as exc_info:
                sanitize_text_input(pattern)
            assert 'command' in str(exc_info.value).lower() or 'dangerous' in str(exc_info.value).lower()

    def test_long_text_truncated(self):
        """Test very long text is truncated."""
        long_text = 'a' * 20000
        safe = sanitize_text_input(long_text, max_length=5000)
        assert len(safe) == 5000

    def test_text_with_newlines(self):
        """Test text with newlines is preserved."""
        text = "Line 1\nLine 2\nLine 3"
        assert sanitize_text_input(text) == text


@pytest.mark.unit
@pytest.mark.security
class TestURLValidation:
    """Tests for URL validation."""

    def test_valid_http_url(self):
        """Test valid HTTP URL."""
        is_valid, msg = validate_url('http://example.com')
        assert is_valid is True
        assert msg == ''

    def test_valid_https_url(self):
        """Test valid HTTPS URL."""
        is_valid, msg = validate_url('https://example.com/path?query=1')
        assert is_valid is True
        assert msg == ''

    def test_invalid_url_format(self):
        """Test invalid URL format."""
        is_valid, msg = validate_url('not a url')
        assert is_valid is False
        assert 'Invalid URL' in msg

    def test_localhost_blocked(self):
        """Test localhost URLs are blocked."""
        is_valid, msg = validate_url('http://localhost:8000')
        assert is_valid is False
        assert 'localhost' in msg.lower() or 'internal' in msg.lower()

    def test_loopback_ip_blocked(self):
        """Test loopback IP is blocked."""
        is_valid, msg = validate_url('http://127.0.0.1')
        assert is_valid is False
        assert 'internal' in msg.lower() or 'localhost' in msg.lower()

    def test_private_ip_blocked(self):
        """Test private IP ranges are blocked."""
        private_ips = [
            'http://192.168.1.1',
            'http://10.0.0.1',
            'http://172.16.0.1',
        ]

        for ip in private_ips:
            is_valid, msg = validate_url(ip)
            assert is_valid is False
            assert 'internal' in msg.lower()

    def test_file_scheme_blocked(self):
        """Test file:// scheme is blocked."""
        is_valid, msg = validate_url('file:///etc/passwd')
        assert is_valid is False
        assert 'not allowed' in msg.lower()

    def test_ftp_scheme_blocked(self):
        """Test ftp:// scheme is blocked."""
        is_valid, msg = validate_url('ftp://example.com')
        assert is_valid is False
        assert 'not allowed' in msg.lower()

    def test_url_too_long(self):
        """Test very long URL is rejected."""
        long_url = 'https://example.com/' + 'a' * 3000
        is_valid, msg = validate_url(long_url)
        assert is_valid is False
        assert 'too long' in msg.lower()


@pytest.mark.unit
@pytest.mark.security
class TestSafeFilePath:
    """Tests for safe file path generation."""

    def test_generates_safe_path(self, temp_directory):
        """Test that safe path is generated."""
        path = get_safe_file_path(temp_directory, 12345, 'document.pdf')

        assert temp_directory in path
        assert '12345' in path
        assert 'document' in path
        assert '.pdf' in path
        assert os.path.dirname(path) == os.path.join(temp_directory, '12345')

    def test_creates_user_directory(self, temp_directory):
        """Test that user directory is created."""
        path = get_safe_file_path(temp_directory, 12345, 'document.pdf')
        user_dir = os.path.join(temp_directory, '12345')

        assert os.path.exists(user_dir)
        assert os.path.isdir(user_dir)

    def test_sanitizes_filename(self, temp_directory):
        """Test that filename is sanitized in path."""
        dangerous_name = '../../etc/passwd'
        path = get_safe_file_path(temp_directory, 12345, dangerous_name)

        assert '..' not in path
        assert 'etc' not in path or 'passwd' in path  # Should be sanitized

    def test_unique_filenames(self, temp_directory):
        """Test that multiple calls generate unique filenames."""
        path1 = get_safe_file_path(temp_directory, 12345, 'document.pdf')
        path2 = get_safe_file_path(temp_directory, 12345, 'document.pdf')

        # Should have timestamp in name making them unique
        assert path1 != path2


@pytest.mark.unit
@pytest.mark.security
class TestIntegratedFileValidation:
    """Tests for complete file validation."""

    def test_valid_pdf_file(self, sample_pdf_file):
        """Test validation of valid PDF file."""
        filename = os.path.basename(sample_pdf_file)
        is_valid, msg = validate_file(sample_pdf_file, filename, 'pdf')
        assert is_valid is True
        assert msg == ''

    def test_invalid_extension_fails(self, temp_directory):
        """Test file with wrong extension fails validation."""
        bad_file = os.path.join(temp_directory, 'malware.exe')
        with open(bad_file, 'wb') as f:
            f.write(b'test content')

        is_valid, msg = validate_file(bad_file, 'malware.exe', 'pdf')
        assert is_valid is False
        assert 'extension' in msg.lower() or '.exe' in msg

    def test_empty_file_fails(self, temp_directory):
        """Test empty file fails validation."""
        empty_file = os.path.join(temp_directory, 'empty.pdf')
        with open(empty_file, 'w') as f:
            pass

        is_valid, msg = validate_file(empty_file, 'empty.pdf', 'pdf')
        assert is_valid is False
        assert 'empty' in msg.lower()
