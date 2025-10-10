from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.models import Usuarios, NivelUsuarios
from app.schemas.schemas import TokenData

# Configuración de encriptación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Mapeo de niveles de usuario a roles
USER_ROLES = {
    1: "administrador",
    2: "supervisor", 
    3: "cca",
    4: "app"
}

def verify_password(plain_password, hashed_password):
    """Verificar contraseña"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Obtener hash de contraseña"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crear token de acceso JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, user_id: int, password: str):
    """Autenticar usuario"""
    user = db.query(Usuarios).filter(
        Usuarios.IdUsuarios == user_id,
        Usuarios.Estatus == 1  # Solo usuarios activos
    ).first()
    
    if not user:
        return False
    
    # Verificar contraseña (por ahora sin hash, como en la BD original)
    # En producción debería usar hashing
    if user.Contraseña != password:
        return False
    
    return user

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Obtener usuario actual desde el token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    user = db.query(Usuarios).filter(
        Usuarios.IdUsuarios == token_data.user_id,
        Usuarios.Estatus == 1
    ).first()
    
    if user is None:
        raise credentials_exception
    
    return user

def get_user_role(user: Usuarios) -> str:
    """Obtener el rol del usuario"""
    return USER_ROLES.get(user.NivelUsuario, "desconocido")

def require_roles(allowed_roles: list):
    """Decorador para requerir roles específicos"""
    def role_checker(current_user: Usuarios = Depends(get_current_user)):
        user_role = get_user_role(current_user)
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere uno de los siguientes roles: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker

# Dependencias específicas por rol
def require_admin(current_user: Usuarios = Depends(require_roles(["administrador"]))):
    return current_user

def require_admin_or_supervisor(current_user: Usuarios = Depends(require_roles(["administrador", "supervisor"]))):
    return current_user

def require_admin_cca_supervisor(current_user: Usuarios = Depends(require_roles(["administrador", "cca", "supervisor"]))):
    return current_user

def require_any_user(current_user: Usuarios = Depends(require_roles(["administrador", "supervisor", "cca", "app"]))):
    return current_user
