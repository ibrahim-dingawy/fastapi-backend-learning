from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.user_service import (
    authenticate_user,
    create_user,
    get_current_user,
    require_admin
)
from app.core.security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_user(
            db=db,
            name=user_data.name,
            email=user_data.email,
            password=user_data.password,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )



@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db=db,
        email=form_data.username,
        password=form_data.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        user_id=user.id
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_my_profile(
    current_user=Depends(get_current_user),
):
    return current_user


@router.get("/admin-test")
def admin_test(
    current_admin=Depends(require_admin),
):
    return {
        "message": "Welcome admin",
        "admin": current_admin.email,
    }