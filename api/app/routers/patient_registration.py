"""Public online patient-registration endpoints.

Drafts are protected by an opaque resume token. Only a SHA-256 hash of that
token is stored. Request bodies are never logged by the application.
"""

import datetime
import hashlib
import secrets

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.patient_registration import PatientRegistration
from app.schemas.patient_registration import (
    RegistrationCreate,
    RegistrationCreatedResponse,
    RegistrationResponse,
    RegistrationSubmitResponse,
    RegistrationUpdate,
)

router = APIRouter(tags=["patient-registration"])


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _new_reference() -> str:
    return "REG-" + secrets.token_hex(5).upper()


def _registration_or_404(db: Session, reference: str) -> PatientRegistration:
    registration = (
        db.query(PatientRegistration)
        .filter(PatientRegistration.public_reference == reference)
        .first()
    )
    if registration is None:
        raise HTTPException(status_code=404, detail="Registration not found")
    return registration


def _authorize(registration: PatientRegistration, token: str | None) -> None:
    if not token or not secrets.compare_digest(registration.resume_token_hash, _hash_token(token)):
        raise HTTPException(status_code=401, detail="Invalid registration resume token")


def _response(registration: PatientRegistration) -> dict:
    return {
        "public_reference": registration.public_reference,
        "status": registration.status,
        "appointment_reference": registration.appointment_reference,
        "first_name": registration.first_name,
        "last_name": registration.last_name,
        "date_of_birth": registration.date_of_birth,
        "email": registration.email,
        "phone": registration.phone,
        "address_line1": registration.address_line1,
        "address_line2": registration.address_line2,
        "city": registration.city,
        "state": registration.state,
        "postal_code": registration.postal_code,
        "emergency_contact_name": registration.emergency_contact_name,
        "emergency_contact_phone": registration.emergency_contact_phone,
        "privacy_acknowledged": registration.privacy_acknowledged,
        "updated_at": registration.updated_at,
        "submitted_at": registration.submitted_at,
    }


@router.post("/patient-registrations", response_model=RegistrationCreatedResponse, status_code=201)
def create_registration(payload: RegistrationCreate, db: Session = Depends(get_db)):
    token = secrets.token_urlsafe(32)
    reference = _new_reference()
    while db.query(PatientRegistration).filter(PatientRegistration.public_reference == reference).first():
        reference = _new_reference()

    registration = PatientRegistration(
        public_reference=reference,
        resume_token_hash=_hash_token(token),
        **payload.model_dump(),
    )
    db.add(registration)
    db.commit()
    db.refresh(registration)
    data = _response(registration)
    data["resume_token"] = token
    return data


@router.get("/patient-registrations/{reference}", response_model=RegistrationResponse)
def get_registration(
    reference: str,
    x_registration_token: str | None = Header(default=None, alias="X-Registration-Token"),
    db: Session = Depends(get_db),
):
    registration = _registration_or_404(db, reference)
    _authorize(registration, x_registration_token)
    return _response(registration)


@router.patch("/patient-registrations/{reference}", response_model=RegistrationResponse)
def save_registration(
    reference: str,
    payload: RegistrationUpdate,
    x_registration_token: str | None = Header(default=None, alias="X-Registration-Token"),
    db: Session = Depends(get_db),
):
    registration = _registration_or_404(db, reference)
    _authorize(registration, x_registration_token)
    if registration.status == "submitted":
        raise HTTPException(status_code=409, detail="Submitted registration cannot be edited")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(registration, key, value)
    registration.updated_at = datetime.datetime.now(datetime.timezone.utc)
    db.commit()
    db.refresh(registration)
    return _response(registration)


@router.post(
    "/patient-registrations/{reference}/submit",
    response_model=RegistrationSubmitResponse,
)
def submit_registration(
    reference: str,
    x_registration_token: str | None = Header(default=None, alias="X-Registration-Token"),
    db: Session = Depends(get_db),
):
    registration = _registration_or_404(db, reference)
    _authorize(registration, x_registration_token)

    required = {
        "first_name": registration.first_name,
        "last_name": registration.last_name,
        "date_of_birth": registration.date_of_birth,
        "email": registration.email,
        "phone": registration.phone,
        "address_line1": registration.address_line1,
        "city": registration.city,
        "state": registration.state,
        "postal_code": registration.postal_code,
    }
    missing = [name for name, value in required.items() if not value]
    if not registration.privacy_acknowledged:
        missing.append("privacy_acknowledged")
    if missing:
        raise HTTPException(status_code=422, detail={"message": "Registration is incomplete", "missing": missing})

    if registration.status != "submitted":
        now = datetime.datetime.now(datetime.timezone.utc)
        registration.status = "submitted"
        registration.submitted_at = now
        registration.updated_at = now
        db.commit()
        db.refresh(registration)

    return {
        "public_reference": registration.public_reference,
        "status": registration.status,
        "submitted_at": registration.submitted_at,
    }
