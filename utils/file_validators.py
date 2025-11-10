"""
File validation utilities for secure uploads
"""
from fastapi import UploadFile
import os
from typing import Dict

# Allowed file types and extensions
ALLOWED_EXTENSIONS = {
    'pdf': ['.pdf'],
    'excel': ['.xlsx', '.xls', '.csv'],
    'word': ['.docx', '.doc'],
    'audio': ['.mp3', '.wav', '.m4a', '.ogg'],
    'text': ['.txt'],
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.webp']
}

# Max file size: 50MB
MAX_FILE_SIZE = 50 * 1024 * 1024

# Allowed MIME types
ALLOWED_MIME_TYPES = {
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-excel',
    'text/csv',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/msword',
    'audio/mpeg',
    'audio/wav',
    'audio/mp4',
    'audio/ogg',
    'text/plain',
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp'
}


def validate_file_upload(file: UploadFile) -> Dict[str, any]:
    """
    Validate uploaded file

    Args:
        file: FastAPI UploadFile object

    Returns:
        Dictionary with validation result:
        {
            "valid": bool,
            "error": str (if not valid),
            "file_type": str (document type)
        }
    """
    # Check if file exists
    if not file:
        return {"valid": False, "error": "No file provided"}

    # Get file extension
    file_extension = os.path.splitext(file.filename)[1].lower()

    # Validate extension
    file_type = None
    for doc_type, extensions in ALLOWED_EXTENSIONS.items():
        if file_extension in extensions:
            file_type = doc_type
            break

    if not file_type:
        return {
            "valid": False,
            "error": f"File type not supported. Allowed extensions: {', '.join([ext for exts in ALLOWED_EXTENSIONS.values() for ext in exts])}"
        }

    # Validate MIME type (if provided)
    if file.content_type and file.content_type not in ALLOWED_MIME_TYPES:
        return {
            "valid": False,
            "error": f"Invalid MIME type: {file.content_type}"
        }

    return {
        "valid": True,
        "file_type": file_type
    }


def validate_file_size(file_path: str) -> bool:
    """
    Validate file size after it's been saved

    Args:
        file_path: Path to the saved file

    Returns:
        True if file size is valid, False otherwise
    """
    if not os.path.exists(file_path):
        return False

    file_size = os.path.getsize(file_path)
    return file_size <= MAX_FILE_SIZE


# ============================================================================
# Additional validation functions for testing and security
# ============================================================================

def is_valid_pdf(file_path: str) -> bool:
    """
    Validate if file is a valid PDF.

    Args:
        file_path: Path to the PDF file

    Returns:
        True if valid PDF, False otherwise
    """
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return False

    try:
        import fitz  # PyMuPDF
        with fitz.open(file_path) as doc:
            # Try to access basic properties
            _ = doc.page_count
            return True
    except Exception:
        return False


def is_valid_excel(file_path: str) -> bool:
    """
    Validate if file is a valid Excel file.

    Args:
        file_path: Path to the Excel file

    Returns:
        True if valid Excel, False otherwise
    """
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return False

    try:
        import pandas as pd
        # Try to read the file
        pd.read_excel(file_path, nrows=0)
        return True
    except Exception:
        return False


def is_valid_word(file_path: str) -> bool:
    """
    Validate if file is a valid Word document.

    Args:
        file_path: Path to the Word file

    Returns:
        True if valid Word document, False otherwise
    """
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return False

    try:
        from docx import Document
        doc = Document(file_path)
        # Try to access basic properties
        _ = len(doc.paragraphs)
        return True
    except Exception:
        return False


def is_valid_audio(file_path: str) -> bool:
    """
    Validate if file is a valid audio file.

    Args:
        file_path: Path to the audio file

    Returns:
        True if valid audio, False otherwise
    """
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return False

    try:
        from pydub import AudioSegment
        # Try to load the audio file
        audio = AudioSegment.from_file(file_path)
        return len(audio) > 0
    except Exception:
        return False


def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in megabytes.

    Args:
        file_path: Path to the file

    Returns:
        File size in MB, or 0.0 if file doesn't exist
    """
    if not os.path.exists(file_path):
        return 0.0

    file_size_bytes = os.path.getsize(file_path)
    return file_size_bytes / (1024 * 1024)


def sanitize_file_path(file_path: str) -> str:
    """
    Sanitize file path to prevent path traversal and other attacks.

    Args:
        file_path: File path to sanitize

    Returns:
        Sanitized file path
    """
    # Remove null bytes
    file_path = file_path.replace('\x00', '')

    # Normalize path
    file_path = os.path.normpath(file_path)

    # Remove path traversal attempts
    file_path = file_path.replace('..', '')

    return file_path
