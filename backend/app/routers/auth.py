import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

SECRET_KEY = os.getenv("SECRET_KEY", "viridis-secure-jwt-secret-key-2026-sustainability")
SALT = "viridis-salt-"


def hash_password(password: str) -> str:
    """Secure salted PBKDF2-HMAC password hashing."""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), (SALT + salt).encode("utf-8"), 100000)
    return f"{salt}${key.hex()}"


def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verifies a plain password against the stored salt$hash."""
    try:
        if "$" not in stored_password:
            # Fallback for plain or simple legacy hashes
            return stored_password == provided_password

        salt, key_hex = stored_password.split("$", 1)
        test_key = hashlib.pbkdf2_hmac("sha256", provided_password.encode("utf-8"), (SALT + salt).encode("utf-8"), 100000)
        return hmac.compare_digest(key_hex, test_key.hex())
    except Exception:
        return False


def create_access_token(data: dict, expires_in_seconds: int = 86400 * 7) -> str:
    """Generates an HMAC-SHA256 signed JWT token."""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = data.copy()
    payload["exp"] = int(time.time()) + expires_in_seconds

    def b64url(d: dict) -> str:
        s = json.dumps(d, separators=(",", ":")).encode("utf-8")
        return base64.urlsafe_b64encode(s).decode("utf-8").rstrip("=")

    h_b64 = b64url(header)
    p_b64 = b64url(payload)
    message = f"{h_b64}.{p_b64}".encode("utf-8")
    sig = hmac.new(SECRET_KEY.encode("utf-8"), message, hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(sig).decode("utf-8").rstrip("=")
    return f"{h_b64}.{p_b64}.{sig_b64}"


def decode_access_token(token: str) -> Optional[dict]:
    """Decodes and verifies an HMAC-SHA256 signed JWT token."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None

        h_b64, p_b64, sig_b64 = parts
        message = f"{h_b64}.{p_b64}".encode("utf-8")
        expected_sig = hmac.new(SECRET_KEY.encode("utf-8"), message, hashlib.sha256).digest()
        actual_sig = base64.urlsafe_b64decode(sig_b64 + "==")

        if not hmac.compare_digest(expected_sig, actual_sig):
            return None

        payload_bytes = base64.urlsafe_b64decode(p_b64 + "==")
        payload = json.loads(payload_bytes.decode("utf-8"))

        if payload.get("exp", 0) < time.time():
            return None  # Expired

        return payload
    except Exception:
        return None


@router.post("/register", response_model=schemas.AuthResponse, status_code=status.HTTP_201_CREATED)
def register(req: schemas.UserRegister, db: Session = Depends(get_db)):
    clean_email = req.email.strip().lower()

    existing_user = db.query(models.User).filter(models.User.email == clean_email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address is already registered.",
        )

    # Create Hospital profile
    hospital = models.Hospital(
        name=req.hospitalName.strip(),
        location=req.location.strip() if req.location else "Main Campus",
        type=req.hospitalType.strip() if req.hospitalType else "Multi-Speciality",
        beds=250,
    )
    db.add(hospital)
    db.commit()
    db.refresh(hospital)

    # Create User account
    hashed_pwd = hash_password(req.password)
    user = models.User(
        email=clean_email,
        hashed_password=hashed_pwd,
        full_name=req.hospitalName.strip(),
        phone=req.phone.strip() if req.phone else None,
        role="admin",
        hospital_id=hospital.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id), "email": user.email, "hospital_id": hospital.id})

    return schemas.AuthResponse(
        access_token=token,
        token_type="bearer",
        user=schemas.UserRead.model_validate(user),
        hospital=schemas.HospitalRead.model_validate(hospital),
    )


@router.post("/login", response_model=schemas.AuthResponse)
def login(req: schemas.UserLogin, db: Session = Depends(get_db)):
    clean_email = req.email.strip().lower()

    user = db.query(models.User).filter(models.User.email == clean_email).first()
    if not user or not verify_password(user.hashed_password, req.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password. Please verify your credentials.",
        )

    hospital = db.get(models.Hospital, user.hospital_id) if user.hospital_id else None

    token = create_access_token({"sub": str(user.id), "email": user.email, "hospital_id": user.hospital_id})

    return schemas.AuthResponse(
        access_token=token,
        token_type="bearer",
        user=schemas.UserRead.model_validate(user),
        hospital=schemas.HospitalRead.model_validate(hospital) if hospital else None,
    )


@router.get("/me", response_model=schemas.AuthResponse)
def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token header")

    token = authorization.split(" ", 1)[1]
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or invalid")

    user_id = int(payload["sub"])
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    hospital = db.get(models.Hospital, user.hospital_id) if user.hospital_id else None

    return schemas.AuthResponse(
        access_token=token,
        token_type="bearer",
        user=schemas.UserRead.model_validate(user),
        hospital=schemas.HospitalRead.model_validate(hospital) if hospital else None,
    )
