from datetime import timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.core.security import authenticate_user, create_access_token, get_user_role, get_current_user
from app.schemas.schemas import Token, UsuarioLogin, UsuarioResponse
from app.models.models import Usuarios

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
    usuario_data: UsuarioLogin,
    db: Session = Depends(get_db)
):
    """Iniciar sesión y obtener token de acceso"""
    
    user = authenticate_user(db, usuario_data.IdUsuarios, usuario_data.Contraseña)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ID de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.IdUsuarios)}, expires_delta=access_token_expires
    )
    
    user_info = UsuarioResponse(
        IdUsuarios=user.IdUsuarios,
        NombreUsuario=user.NombreUsuario,
        NivelUsuario=user.NivelUsuario,
        Estatus=user.Estatus
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_info": user_info
    }

@router.get("/me", response_model=UsuarioResponse)
async def read_users_me(
    current_user = Depends(get_current_user)
):
    """Obtener información del usuario actual"""
    return UsuarioResponse(
        IdUsuarios=current_user.IdUsuarios,
        NombreUsuario=current_user.NombreUsuario,
        NivelUsuario=current_user.NivelUsuario,
        Estatus=current_user.Estatus
    )

@router.get("/role")
async def get_my_role(
    current_user = Depends(get_current_user)
):
    """Obtener el rol del usuario actual"""
    return {
        "user_id": current_user.IdUsuarios,
        "role": get_user_role(current_user),
        "level": current_user.NivelUsuario
    }

@router.get("/usuarios", response_model=List[UsuarioResponse])
async def get_usuarios(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener lista de usuarios activos para asignación"""
    usuarios = db.query(Usuarios).filter(Usuarios.Estatus == 1).all()
    return [UsuarioResponse(
        IdUsuarios=usuario.IdUsuarios,
        NombreUsuario=usuario.NombreUsuario,
        NivelUsuario=usuario.NivelUsuario,
        Estatus=usuario.Estatus
    ) for usuario in usuarios]
