import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from typing import Callable, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Request, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication & RBAC"])

SECRET_KEY = os.getenv("SECRET_KEY", "viridis-enterprise-jwt-signing-secret-key-2026-v1")
SALT = os.getenv("PASSWORD_SALT", "viridis-secure-salt-2026-")

VALID_ROLES = {"super_admin", "hospital_admin", "department_manager", "auditor"}


def hash_password(password: str) -> str:
    """Secure salted PBKDF2-HMAC password hashing."""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), (SALT + salt).encode("utf-8"), 100000)
    return f"{salt}${key.hex()}"


def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verifies a plain password against the stored salt$hash."""
    try:
        if "$" not in stored_password:
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


def record_audit_log(
    db: Session,
    action: str,
    hospital_id: Optional[int] = None,
    user_id: Optional[int] = None,
    entity_type: Optional[str] = None,
    details: Optional[str] = None,
    ip_address: Optional[str] = None,
):
    """Persists an audit log entry into database."""
    try:
        log_entry = models.AuditLog(
            hospital_id=hospital_id,
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            details=details,
            ip_address=ip_address,
        )
        db.add(log_entry)
        db.commit()
    except Exception:
        db.rollback()


# ---------- AUTHENTICATION & RBAC DEPENDENCIES ----------

def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> models.User:
    """Dependency extracting and validating current user from Bearer token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or malformed Authorization header. Please log in.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.split(" ", 1)[1]
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has expired or is invalid. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    sub_val = payload["sub"]
    if isinstance(sub_val, int) or (isinstance(sub_val, str) and sub_val.isdigit()):
        user = db.get(models.User, int(sub_val))
    else:
        user = db.query(models.User).filter(models.User.email == str(sub_val)).first()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive or not found.",
        )

    return user



def require_roles(*allowed_roles: str) -> Callable:
    """RBAC Dependency generator ensuring user has at least one of the required roles."""
    def role_checker(current_user: models.User = Depends(get_current_user)) -> models.User:
        if current_user.role == "super_admin":
            return current_user  # Super Admin has cross-cutting permissions

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role in {allowed_roles}, but current user has role '{current_user.role}'.",
            )
        return current_user

    return role_checker


def validate_hospital_access(hospital_id: int, current_user: models.User) -> bool:
    """Validates that current user is authorized to view/manage the requested hospital."""
    if current_user.role == "super_admin":
        return True
    if current_user.hospital_id != hospital_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You do not have permission to access data for this hospital.",
        )
    return True


# ---------- API ENDPOINTS ----------

@router.post("/register", response_model=schemas.AuthResponse, status_code=status.HTTP_201_CREATED)
def register(req: schemas.UserRegister, request: Request, db: Session = Depends(get_db)):
    clean_email = req.email.strip().lower()

    existing_user = db.query(models.User).filter(models.User.email == clean_email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address is already registered.",
        )

    assigned_role = req.role if req.role in VALID_ROLES else "hospital_admin"

    # Create Hospital profile
    hospital = models.Hospital(
        name=req.hospitalName.strip(),
        location=req.location.strip() if req.location else "Main Campus",
        type=req.hospitalType.strip() if req.hospitalType else "Multi-Speciality Tertiary Care",
        beds=250,
        occupied_beds_avg=210.0,
        total_area_sqft=175000.0,
    )
    db.add(hospital)
    db.commit()
    db.refresh(hospital)

    # Add default standard hospital departments
    default_depts = ["Intensive Care Unit (ICU)", "Operation Theatres", "Inpatient Wards", "Radiology & Imaging", "Diagnostic Labs", "Central Sterile Supply (CSSD)", "Facilities & HVAC"]
    for dept_name in default_depts:
        db.add(models.Department(hospital_id=hospital.id, name=dept_name))
    db.commit()

    # Create User account
    hashed_pwd = hash_password(req.password)
    user = models.User(
        email=clean_email,
        hashed_password=hashed_pwd,
        full_name=req.hospitalName.strip() + " Administrator",
        phone=req.phone.strip() if req.phone else None,
        role=assigned_role,
        hospital_id=hospital.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    client_ip = request.client.host if request and request.client else None
    record_audit_log(db, "USER_REGISTER", hospital.id, user.id, "AUTH", f"Registered hospital '{hospital.name}' with admin role '{assigned_role}'", client_ip)

    token = create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
        "hospital_id": hospital.id,
    })

    return schemas.AuthResponse(
        access_token=token,
        token_type="bearer",
        user=schemas.UserRead.model_validate(user),
        hospital=schemas.HospitalRead.model_validate(hospital),
    )


@router.post("/login", response_model=schemas.AuthResponse)
def login(req: schemas.UserLogin, request: Request, db: Session = Depends(get_db)):
    clean_email = req.email.strip().lower()

    user = db.query(models.User).filter(models.User.email == clean_email).first()
    if not user or not verify_password(user.hashed_password, req.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password. Please verify your credentials.",
        )

    hospital = db.get(models.Hospital, user.hospital_id) if user.hospital_id else None

    token = create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
        "hospital_id": user.hospital_id,
    })

    client_ip = request.client.host if request and request.client else None
    record_audit_log(db, "LOGIN_SUCCESS", user.hospital_id, user.id, "AUTH", f"User {user.email} successfully logged in", client_ip)


    return schemas.AuthResponse(
        access_token=token,
        token_type="bearer",
        user=schemas.UserRead.model_validate(user),
        hospital=schemas.HospitalRead.model_validate(hospital) if hospital else None,
    )


@router.get("/me", response_model=schemas.AuthResponse)
def get_current_user_profile(
    current_user: models.User = Depends(get_current_user),
    authorization: str = Header(...),
    db: Session = Depends(get_db),
):
    token = authorization.split(" ", 1)[1]
    hospital = db.get(models.Hospital, current_user.hospital_id) if current_user.hospital_id else None

    return schemas.AuthResponse(
        access_token=token,
        token_type="bearer",
        user=schemas.UserRead.model_validate(current_user),
        hospital=schemas.HospitalRead.model_validate(hospital) if hospital else None,
    )


@router.get("/users", response_model=List[schemas.UserRead])
def list_hospital_users(
    current_user: models.User = Depends(require_roles("super_admin", "hospital_admin")),
    db: Session = Depends(get_db),
):
    """List users belonging to current user's hospital (or all users for super_admin)."""
    if current_user.role == "super_admin":
        return db.query(models.User).all()
    return db.query(models.User).filter(models.User.hospital_id == current_user.hospital_id).all()


@router.post("/users", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_hospital_user(
    req: schemas.UserCreateInternal,
    current_user: models.User = Depends(require_roles("super_admin", "hospital_admin")),
    db: Session = Depends(get_db),
):
    """Create a sub-user (e.g., department manager or auditor) under current hospital."""
    clean_email = req.email.strip().lower()
    if db.query(models.User).filter(models.User.email == clean_email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hosp_id = req.hospital_id if current_user.role == "super_admin" and req.hospital_id else current_user.hospital_id

    role = req.role if req.role in VALID_ROLES else "department_manager"
    # Hospital admin cannot create super_admin
    if current_user.role != "super_admin" and role == "super_admin":
        role = "department_manager"

    new_user = models.User(
        email=clean_email,
        hashed_password=hash_password(req.password),
        full_name=req.full_name,
        phone=req.phone,
        role=role,
        hospital_id=hosp_id,
        department_id=req.department_id,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    record_audit_log(db, "USER_CREATED", hosp_id, current_user.id, "USER", f"Created user {clean_email} with role {role}")
    return new_user


@router.get("/audit-logs", response_model=List[schemas.AuditLogRead])
def get_audit_logs(
    limit: int = 50,
    current_user: models.User = Depends(require_roles("super_admin", "hospital_admin", "auditor")),
    db: Session = Depends(get_db),
):
    """Retrieve audit logs for hospital compliance reviews."""
    query = db.query(models.AuditLog)
    if current_user.role != "super_admin":
        query = query.filter(models.AuditLog.hospital_id == current_user.hospital_id)
    return query.order_by(models.AuditLog.timestamp.desc()).limit(limit).all()

