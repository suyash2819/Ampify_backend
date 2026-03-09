from fastapi import APIRouter, HTTPException, status

from core.security import create_access_token, verify_password
from repositories.users_repo import users_repo
from schemas.auth import SigninRequest, TokenResponse
from schemas.user import UserOut, UserCreate

router = APIRouter(prefix="/user", tags=["auth"],)


@router.post("/signin", response_model=TokenResponse)
def signin(payload: SigninRequest):
    user = users_repo.get_user_with_password_by_email(payload.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)

@router.post("/signup", response_model=UserOut)
def signup(payload: UserCreate):
    """Register a new user."""
    # Check if user already exists
    existing_user = users_repo.get_user_by_email(payload.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    new_user = users_repo.create_user(payload)
    return new_user
