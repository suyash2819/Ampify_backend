from fastapi import APIRouter, HTTPException, status

from core.security import create_access_token, verify_password
from repositories.memory_repo import repo
from schemas.auth import SigninRequest, TokenResponse

router = APIRouter(prefix="/user")


@router.post("/signin", response_model=TokenResponse)
def signin(payload: SigninRequest):
    user = repo.get_user_by_email(payload.email)
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
