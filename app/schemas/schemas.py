from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional
from enum import Enum

class UserRole(str, Enum):
    ADMINISTRADOR = "administrador"
    APP = "app"
    CCA = "cca"
    SUPERVISOR = "supervisor"

# Schemas para productos/catálogo
class ProductoBase(BaseModel):
    CodigoBarras: str
    Producto: str
    IdMaterial: str
    IdFamilia: int
    IdCategoria: int
    IdSubcategoria: int

class ProductoResponse(ProductoBase):
    class Config:
        from_attributes = True

# Schemas para conteo detalles
class ConteoDetalleBase(BaseModel):
    CodigoBarras: str = Field(..., description="Código de barras del producto")
    NSistema: float = Field(..., description="Número de existencias en sistema")
    NExcistencia: float = Field(..., description="Número de existencias físicas")

class ConteoDetalleCreate(ConteoDetalleBase):
    pass

class ConteoDetalleUpdate(BaseModel):
    CodigoBarras: str = Field(..., description="Código de barras del producto")
    NExcistencia: Optional[float] = Field(None, description="Número de existencias físicas (solo para contestar)")

class ConteoDetalleResponse(ConteoDetalleBase):
    idConteoDetalles: int
    IdConteo: int
    
    class Config:
        from_attributes = True

# Schemas para conteos
class ConteoBase(BaseModel):
    IdCentro: str = Field(..., description="ID del centro/sucursal")

class ConteoCreate(ConteoBase):
    """Schema para crear un nuevo conteo"""
    detalles: List[ConteoDetalleCreate] = Field(..., description="Lista de productos a contar")

class ConteoAsignar(ConteoBase):
    """Schema para asignar un conteo a otro usuario"""
    Fechal: Optional[date] = Field(None, description="Fecha del conteo (opcional, por defecto fecha actual)")
    IdUsuario: int = Field(..., description="ID del usuario al que se asigna el conteo")
    detalles: List[ConteoDetalleCreate] = Field(..., description="Lista de productos a contar")

class ConteoEdit(BaseModel):
    """Schema para editar un conteo existente"""
    Fechal: Optional[date] = None
    IdCentro: Optional[str] = None
    IdUsuario: Optional[int] = None
    detalles: Optional[List[ConteoDetalleCreate]] = None

class ConteoContestar(BaseModel):
    """Schema para contestar un conteo (modificar existencias físicas)"""
    detalles: List[ConteoDetalleUpdate] = Field(..., description="Lista de actualizaciones de existencias")

class ConteoResponse(BaseModel):
    idConteo: int
    Fechal: date
    Envio: int
    IdRealizo: int
    IdCentro: str
    IdUsuario: int
    detalles: List[ConteoDetalleResponse]
    
    class Config:
        from_attributes = True

class ConteoListResponse(BaseModel):
    idConteo: int
    Fechal: date
    Envio: int
    IdRealizo: int
    IdCentro: str
    IdUsuario: int
    total_productos: int
    
    class Config:
        from_attributes = True

# Schemas para usuarios y autenticación
class UsuarioBase(BaseModel):
    IdUsuarios: int
    NombreUsuario: str
    NivelUsuario: int
    Estatus: int

class UsuarioLogin(BaseModel):
    IdUsuarios: int
    Contraseña: str

class UsuarioResponse(UsuarioBase):
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user_info: UsuarioResponse

class TokenData(BaseModel):
    user_id: Optional[int] = None

# Schemas para sucursales
class SucursalBase(BaseModel):
    IdCentro: str
    Sucursales: str
    IdTipoSucursal: str
    IdZona: int
    IdEstado: int
    Latitud: str
    Longitud: str
    IdMunicipio: int

class SucursalResponse(SucursalBase):
    class Config:
        from_attributes = True

# Schema para respuestas de error
class ErrorResponse(BaseModel):
    detail: str
    code: Optional[str] = None

# Schema para respuestas de éxito
class SuccessResponse(BaseModel):
    message: str
    data: Optional[dict] = None
