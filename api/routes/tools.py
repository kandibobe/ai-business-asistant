"""
Developer tools routes.
JSON validator, Base64, Hash, etc.

SECURITY: All endpoints require authentication (CRITICAL FIX)
"""
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
import json
import base64
import hashlib

from utils.validators import (
    JsonValidateRequest,
    Base64EncodeRequest,
    HashGenerateRequest,
    QRCodeRequest
)
from api.dependencies import get_current_user, get_db
from database.models import User

router = APIRouter()


@router.post("/json/validate")
async def validate_json(
    request: JsonValidateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Validate and format JSON string."""
    try:
        parsed = json.loads(request.json_string)
        formatted = json.dumps(parsed, indent=2, ensure_ascii=False)

        return {
            "valid": True,
            "formatted": formatted,
            "message": "JSON is valid"
        }
    except json.JSONDecodeError as e:
        return {
            "valid": False,
            "error": str(e),
            "message": "Invalid JSON"
        }


@router.post("/base64/encode")
async def encode_base64(
    request: Base64EncodeRequest,
    current_user: User = Depends(get_current_user)
):
    """Encode text to Base64. [AUTH REQUIRED]"""
    encoded = base64.b64encode(request.text.encode()).decode()
    return {"encoded": encoded}


@router.post("/base64/decode")
async def decode_base64(
    encoded: str,
    current_user: User = Depends(get_current_user)
):
    """
    Decode Base64 to text. [AUTH REQUIRED]

    SECURITY FIX: Replaced bare except with specific exception handling.
    """
    try:
        decoded = base64.b64decode(encoded).decode('utf-8')
        return {"decoded": decoded}
    except (base64.binascii.Error, UnicodeDecodeError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Base64 encoding"
        )


@router.post("/hash/{algorithm}")
async def generate_hash(
    request: HashGenerateRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate cryptographic hash of text. [AUTH REQUIRED]

    WARNING: MD5 and SHA1 are deprecated for security. Use SHA256 or SHA512.
    """
    algorithm = request.algorithm.lower()

    # SECURITY: Whitelist of allowed hash algorithms
    hash_funcs = {
        'md5': hashlib.md5,        # Deprecated - for compatibility only
        'sha1': hashlib.sha1,      # Deprecated - for compatibility only
        'sha256': hashlib.sha256,  # Recommended
        'sha512': hashlib.sha512   # Recommended
    }

    if algorithm not in hash_funcs:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported algorithm. Allowed: {', '.join(hash_funcs.keys())}"
        )

    hash_func = hash_funcs[algorithm]
    hash_value = hash_func(request.text.encode('utf-8')).hexdigest()

    return {
        "algorithm": algorithm,
        "hash": hash_value,
        "deprecated": algorithm in ['md5', 'sha1']
    }


@router.post("/qr/generate")
async def generate_qr_code(
    request: QRCodeRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate QR code. [AUTH REQUIRED]

    TODO: Implement QR code generation with qrcode library.
    """
    return {
        "message": "QR code generation not yet implemented",
        "text": request.text,
        "size": request.size
    }
