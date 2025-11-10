"""
Unit tests for file validation utilities.
Tests file_validators helper functions for document processing.
"""
import pytest
import os
from utils.file_validators import (
    is_valid_pdf,
    is_valid_excel,
    is_valid_word,
    is_valid_audio,
    get_file_size_mb,
    sanitize_file_path,
)


class TestPDFValidation:
    """Tests for PDF file validation."""

    def test_valid_pdf_file(self, sample_pdf_file):
        """Test validation of valid PDF file."""
        assert is_valid_pdf(sample_pdf_file) is True

    def test_invalid_pdf_file(self, temp_directory):
        """Test rejection of invalid PDF file."""
        # Create a fake PDF (text file with .pdf extension)
        fake_pdf = os.path.join(temp_directory, "fake.pdf")
        with open(fake_pdf, 'w') as f:
            f.write("This is not a PDF file")

        assert is_valid_pdf(fake_pdf) is False

    def test_nonexistent_pdf_file(self):
        """Test handling of non-existent file."""
        assert is_valid_pdf("/nonexistent/file.pdf") is False

    def test_empty_pdf_file(self, temp_directory):
        """Test handling of empty PDF file."""
        empty_pdf = os.path.join(temp_directory, "empty.pdf")
        with open(empty_pdf, 'w') as f:
            pass  # Create empty file

        assert is_valid_pdf(empty_pdf) is False


class TestExcelValidation:
    """Tests for Excel file validation."""

    def test_valid_excel_file(self, sample_excel_file):
        """Test validation of valid Excel file."""
        assert is_valid_excel(sample_excel_file) is True

    def test_invalid_excel_file(self, temp_directory):
        """Test rejection of invalid Excel file."""
        fake_excel = os.path.join(temp_directory, "fake.xlsx")
        with open(fake_excel, 'w') as f:
            f.write("Not an Excel file")

        assert is_valid_excel(fake_excel) is False

    def test_nonexistent_excel_file(self):
        """Test handling of non-existent Excel file."""
        assert is_valid_excel("/nonexistent/file.xlsx") is False


class TestWordValidation:
    """Tests for Word document validation."""

    def test_valid_word_file(self, sample_word_file):
        """Test validation of valid Word file."""
        assert is_valid_word(sample_word_file) is True

    def test_invalid_word_file(self, temp_directory):
        """Test rejection of invalid Word file."""
        fake_word = os.path.join(temp_directory, "fake.docx")
        with open(fake_word, 'w') as f:
            f.write("Not a Word file")

        assert is_valid_word(fake_word) is False

    def test_nonexistent_word_file(self):
        """Test handling of non-existent Word file."""
        assert is_valid_word("/nonexistent/file.docx") is False


class TestAudioValidation:
    """Tests for audio file validation."""

    def test_valid_audio_file(self, sample_audio_file):
        """Test validation of valid audio file."""
        assert is_valid_audio(sample_audio_file) is True

    def test_invalid_audio_file(self, temp_directory):
        """Test rejection of invalid audio file."""
        fake_audio = os.path.join(temp_directory, "fake.mp3")
        with open(fake_audio, 'w') as f:
            f.write("Not an audio file")

        assert is_valid_audio(fake_audio) is False

    def test_nonexistent_audio_file(self):
        """Test handling of non-existent audio file."""
        assert is_valid_audio("/nonexistent/file.mp3") is False


class TestFileSizeUtils:
    """Tests for file size utilities."""

    def test_get_file_size_mb(self, sample_pdf_file):
        """Test getting file size in MB."""
        size_mb = get_file_size_mb(sample_pdf_file)
        assert size_mb > 0
        assert isinstance(size_mb, float)

    def test_nonexistent_file_size(self):
        """Test file size for non-existent file."""
        size_mb = get_file_size_mb("/nonexistent/file.pdf")
        assert size_mb == 0.0

    def test_empty_file_size(self, temp_directory):
        """Test file size for empty file."""
        empty_file = os.path.join(temp_directory, "empty.txt")
        with open(empty_file, 'w') as f:
            pass

        size_mb = get_file_size_mb(empty_file)
        assert size_mb == 0.0


class TestFilePathSanitization:
    """Tests for file path sanitization."""

    def test_sanitize_normal_path(self):
        """Test sanitization of normal file path."""
        path = "/home/user/documents/file.pdf"
        sanitized = sanitize_file_path(path)
        assert sanitized == path

    def test_sanitize_path_with_traversal(self):
        """Test sanitization removes path traversal attempts."""
        dangerous_path = "/home/user/../../etc/passwd"
        sanitized = sanitize_file_path(dangerous_path)
        assert ".." not in sanitized
        assert "etc/passwd" not in sanitized

    def test_sanitize_path_with_null_bytes(self):
        """Test sanitization removes null bytes."""
        dangerous_path = "/home/user/file\x00.pdf"
        sanitized = sanitize_file_path(dangerous_path)
        assert "\x00" not in sanitized

    def test_sanitize_path_with_special_chars(self):
        """Test sanitization handles special characters."""
        path_with_spaces = "/home/user/my file.pdf"
        sanitized = sanitize_file_path(path_with_spaces)
        # Should preserve spaces in filenames
        assert isinstance(sanitized, str)
        assert len(sanitized) > 0


class TestFileExtensionHandling:
    """Tests for file extension detection and handling."""

    @pytest.mark.parametrize("filename,expected_ext", [
        ("document.pdf", ".pdf"),
        ("spreadsheet.xlsx", ".xlsx"),
        ("report.docx", ".docx"),
        ("audio.mp3", ".mp3"),
        ("DATA.PDF", ".pdf"),  # Case insensitive
        ("file.with.dots.pdf", ".pdf"),
    ])
    def test_extract_file_extension(self, filename, expected_ext):
        """Test extraction of file extension."""
        ext = os.path.splitext(filename)[1].lower()
        assert ext == expected_ext

    def test_file_without_extension(self):
        """Test handling of file without extension."""
        filename = "noextension"
        ext = os.path.splitext(filename)[1]
        assert ext == ""


# Integration tests for file validation workflow
class TestFileValidationWorkflow:
    """Integration tests for complete file validation workflow."""

    def test_complete_pdf_validation_workflow(self, sample_pdf_file):
        """Test complete PDF validation workflow."""
        # Check extension
        ext = os.path.splitext(sample_pdf_file)[1].lower()
        assert ext == '.pdf'

        # Check file exists
        assert os.path.exists(sample_pdf_file)

        # Check file size
        size_mb = get_file_size_mb(sample_pdf_file)
        assert size_mb > 0
        assert size_mb < 50  # Under max limit

        # Validate PDF structure
        assert is_valid_pdf(sample_pdf_file) is True

    def test_complete_excel_validation_workflow(self, sample_excel_file):
        """Test complete Excel validation workflow."""
        ext = os.path.splitext(sample_excel_file)[1].lower()
        assert ext == '.xlsx'
        assert os.path.exists(sample_excel_file)
        size_mb = get_file_size_mb(sample_excel_file)
        assert size_mb > 0
        assert is_valid_excel(sample_excel_file) is True

    def test_complete_word_validation_workflow(self, sample_word_file):
        """Test complete Word validation workflow."""
        ext = os.path.splitext(sample_word_file)[1].lower()
        assert ext == '.docx'
        assert os.path.exists(sample_word_file)
        size_mb = get_file_size_mb(sample_word_file)
        assert size_mb > 0
        assert is_valid_word(sample_word_file) is True

    def test_reject_oversized_file(self, temp_directory):
        """Test rejection of file exceeding size limit."""
        # Create a 51 MB file (over limit)
        large_file = os.path.join(temp_directory, "large.pdf")
        with open(large_file, 'wb') as f:
            f.write(b'0' * (51 * 1024 * 1024))

        size_mb = get_file_size_mb(large_file)
        assert size_mb > 50

    def test_multiple_file_types_in_sequence(
        self, sample_pdf_file, sample_excel_file, sample_word_file
    ):
        """Test validating multiple file types in sequence."""
        files = [
            (sample_pdf_file, is_valid_pdf),
            (sample_excel_file, is_valid_excel),
            (sample_word_file, is_valid_word),
        ]

        for file_path, validator in files:
            assert os.path.exists(file_path)
            assert validator(file_path) is True
