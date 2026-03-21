from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import CreatePrincipalRequest, LoginRequest, TokenResponse, UserResponse
from app.services.auth_service import create_user, get_user_by_email


router = APIRouter()


@router.post("/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = get_user_by_email(db, payload.email)
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    access_token = create_access_token(
        {
            "user_id": str(user.id),
            "role": user.role,
        }
    )
    return TokenResponse(access_token=access_token, token_type="bearer")


@router.post("/admin/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_principal_user(
    payload: CreatePrincipalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    existing_user = get_user_by_email(db, payload.email)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    user = create_user(
        db,
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role="principal",
        school_id=payload.school_id,
    )
    return user
