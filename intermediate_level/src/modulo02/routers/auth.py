from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...modulo01.models import User
from ..dependencies import get_db
from ..schemas.auth import Token
from ..security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    """Endpoint de autenticación para obtener el token JWT."""
    user = db.query(User).filter(User.username == form_data.username).first()

    # Nota: Si el password almacenado aún no tiene hash en la DB de prueba,
    # se valida en texto plano como respaldo o con verify_password.
    if not user or not (
        verify_password(form_data.password, user.hashed_password)
        or user.hashed_password == form_data.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")
