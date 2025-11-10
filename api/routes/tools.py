"""
Developer tools routes.
JSON validator, Base64, Hash, etc.
"""
from fastapi import APIRouter, HTTPException, status
import json
import base64
import hashlib

from utils.validators import (
    JsonValidateRequest,
    Base64EncodeRequest,
    HashGenerateRequest,
    QRCodeRequest
)

router = APIRouter()


@router.post("/json/validate")
async def validate_json(request: JsonValidateRequest):
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
async def encode_base64(request: Base64EncodeRequest):
    """Encode text to Base64."""
    encoded = base64.b64encode(request.text.encode()).decode()
    return {"encoded": encoded}


@router.post("/base64/decode")
async def decode_base64(encoded: str):
    """Decode Base64 to text."""
    try:
        decoded = base64.b64decode(encoded).decode()
        return {"decoded": decoded}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid Base64: {str(e)}"
        )


@router.post("/hash/{algorithm}")
async def generate_hash(request: HashGenerateRequest):
    """Generate hash of text."""
    algorithm = request.algorithm.lower()

    hash_funcs = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512
    }

    if algorithm not in hash_funcs:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported algorithm: {algorithm}"
        )

    hash_func = hash_funcs[algorithm]
    hash_value = hash_func(request.text.encode()).hexdigest()

    return {
        "algorithm": algorithm,
        "hash": hash_value
    }


@router.post("/qr/generate")
async def generate_qr_code(request: QRCodeRequest):
    """
    Generate QR code.

    TODO: Implement QR code generation with qrcode library.
    """
    return {
        "message": "QR code generation not yet implemented",
        "text": request.text,
        "size": request.size
    }
