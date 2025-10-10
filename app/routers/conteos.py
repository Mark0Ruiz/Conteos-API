from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import (
    require_any_user, require_admin_cca_supervisor, 
    require_admin_or_supervisor, require_admin
)
from app.schemas.schemas import (
    ConteoCreate, ConteoAsignar, ConteoEdit, ConteoContestar,
    ConteoResponse, ConteoListResponse, SuccessResponse
)
from app.services.conteo_service import ConteoService
from app.models.models import Usuarios, Sucursales

router = APIRouter()

@router.get("/sucursales", response_model=List[dict])
async def obtener_sucursales(
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(require_any_user)
):
    """Obtener lista de sucursales disponibles"""
    sucursales = db.query(Sucursales).all()
    return [
        {
            "IdCentro": s.IdCentro,
            "Sucursales": s.Sucursales
        }
        for s in sucursales
    ]

@router.post("/crear", response_model=ConteoResponse, status_code=status.HTTP_201_CREATED)
async def crear_conteo(
    conteo_data: ConteoCreate,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(require_any_user)
):
    """
    Crear un nuevo conteo.
    
    **Roles permitidos**: administrador, app, cca, supervisor
    
    **Funcionalidad**:
    - Crea un conteo con fecha actual del sistema
    - Estado 'Envio' se establece en 1 (finalizado) por defecto
    - IdRealizo e IdUsuario son el mismo (quien crea el conteo)
    """
    return ConteoService.crear_conteo(db, conteo_data, current_user.IdUsuarios)

@router.post("/asignar", response_model=ConteoResponse, status_code=status.HTTP_201_CREATED)
async def asignar_conteo(
    conteo_data: ConteoAsignar,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(require_admin_cca_supervisor)
):
    """
    Asignar un conteo a otro usuario.
    
    **Roles permitidos**: administrador, cca, supervisor
    
    **Funcionalidad**:
    - Puede asignar fecha posterior (no anterior a hoy)
    - Estado 'Envio' se establece en 0 (pendiente)
    - IdRealizo es quien asigna, IdUsuario es quien debe contestar
    """
    return ConteoService.asignar_conteo(db, conteo_data, current_user.IdUsuarios)

@router.put("/{conteo_id}/editar", response_model=ConteoResponse)
async def editar_conteo(
    conteo_id: int,
    conteo_data: ConteoEdit,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(require_admin_or_supervisor)
):
    """
    Editar un conteo existente.
    
    **Roles permitidos**: administrador, supervisor
    
    **Restricciones**:
    - Solo se pueden editar conteos con Envio = 0 (pendientes)
    - Si Envio = 1 (finalizado), no se puede modificar nada
    """
    return ConteoService.editar_conteo(db, conteo_id, conteo_data, current_user.IdUsuarios)

@router.put("/{conteo_id}/contestar", response_model=ConteoResponse)
async def contestar_conteo(
    conteo_id: int,
    conteo_data: ConteoContestar,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(require_any_user)
):
    """
    Contestar un conteo (actualizar existencias físicas).
    
    **Roles permitidos**: app, cca, administrador, supervisor
    
    **Funcionalidad**:
    - Solo se pueden contestar conteos con Envio = 0 (pendientes)
    - Permite modificar solo las existencias físicas (NExcistencia)
    - Al contestar, cambia el estado a Envio = 1 (finalizado)
    """
    return ConteoService.contestar_conteo(db, conteo_id, conteo_data, current_user.IdUsuarios)

@router.delete("/{conteo_id}", response_model=SuccessResponse)
async def eliminar_conteo(
    conteo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(require_admin)
):
    """
    Eliminar un conteo.
    
    **Roles permitidos**: administrador únicamente
    
    **Funcionalidad**:
    - Solo los administradores pueden eliminar conteos
    - Elimina el conteo y todos sus detalles asociados
    """
    result = ConteoService.eliminar_conteo(db, conteo_id, current_user.IdUsuarios)
    return SuccessResponse(message=result["message"])

@router.get("/{conteo_id}", response_model=ConteoResponse)
async def obtener_conteo(
    conteo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(require_any_user)
):
    """
    Obtener un conteo específico por ID.
    
    **Roles permitidos**: administrador, app, cca, supervisor
    """
    return ConteoService.obtener_conteo(db, conteo_id)

@router.get("/", response_model=List[ConteoListResponse])
async def listar_conteos(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    id_centro: Optional[str] = Query(None, description="Filtrar por ID de centro/sucursal"),
    envio: Optional[int] = Query(None, ge=0, le=1, description="Filtrar por estado de envío (0=pendiente, 1=finalizado)"),
    id_usuario: Optional[int] = Query(None, description="Filtrar por ID de usuario asignado"),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(require_any_user)
):
    """
    Listar conteos con filtros opcionales.
    
    **Roles permitidos**: administrador, app, cca, supervisor
    
    **Filtros disponibles**:
    - id_centro: Filtrar por sucursal
    - envio: Filtrar por estado (0=pendiente, 1=finalizado)
    - id_usuario: Filtrar por usuario asignado
    - skip/limit: Paginación
    """
    return ConteoService.listar_conteos(
        db=db,
        skip=skip,
        limit=limit,
        id_centro=id_centro,
        envio=envio,
        id_usuario=id_usuario
    )

@router.get("/usuario/{user_id}", response_model=List[ConteoListResponse])
async def obtener_conteos_usuario(
    user_id: int,
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    envio: Optional[int] = Query(None, ge=0, le=1, description="Filtrar por estado de envío"),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(require_any_user)
):
    """
    Obtener conteos asignados a un usuario específico.
    
    **Roles permitidos**: administrador, app, cca, supervisor
    """
    return ConteoService.listar_conteos(
        db=db,
        skip=skip,
        limit=limit,
        id_usuario=user_id,
        envio=envio
    )

@router.get("/sucursal/{centro_id}", response_model=List[ConteoListResponse])
async def obtener_conteos_sucursal(
    centro_id: str,
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    envio: Optional[int] = Query(None, ge=0, le=1, description="Filtrar por estado de envío"),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(require_any_user)
):
    """
    Obtener conteos de una sucursal específica.
    
    **Roles permitidos**: administrador, app, cca, supervisor
    """
    return ConteoService.listar_conteos(
        db=db,
        skip=skip,
        limit=limit,
        id_centro=centro_id,
        envio=envio
    )
