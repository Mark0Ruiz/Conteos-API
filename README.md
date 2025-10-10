# API Conteos SCISP

Sistema de gestión de conteos de productos para sucursales desarrollado con FastAPI.

## Características

- **Framework**: FastAPI con SQLAlchemy
- **Base de datos**: MySQL
- **Autenticación**: JWT con roles (administrador, supervisor, cca, app)
- **Documentación**: Swagger UI automática

## Estructura del Proyecto

```
App_Conteo/
├── app/
│   ├── core/           # Configuración y utilidades centrales
│   ├── models/         # Modelos SQLAlchemy
│   ├── schemas/        # Schemas Pydantic
│   ├── routers/        # Endpoints de la API
│   ├── services/       # Lógica de negocio
├── main.py            # Aplicación principal
├── requirements.txt   # Dependencias
└── .env              # Variables de entorno
```

## Instalación

1. **Clonar el repositorio**
```bash
git clone <url-repositorio>
cd App_Conteo
```

2. **Crear entorno virtual**
```bash
python -m venv venv
venv\Scripts\activate  # En Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos**
- Crear la base de datos MySQL `conteos_scisp`
- Ejecutar el script SQL `conteos_estructura.sql`
- Configurar variables de entorno en `.env`

5. **Configurar variables de entorno**
Editar el archivo `.env`:
```
DATABASE_URL=mysql+pymysql://usuario:password@localhost:3306/conteos_scisp
SECRET_KEY=tu_clave_secreta_muy_segura_aqui_cambiala
```

## Ejecución

### Desarrollo
```bash
python run_dev.py
```

### Producción
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

La API estará disponible en: http://localhost:8000

## Documentación de la API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints Principales

### Autenticación
- `POST /api/v1/auth/login` - Iniciar sesión
- `GET /api/v1/auth/me` - Obtener usuario actual
- `GET /api/v1/auth/role` - Obtener rol del usuario

### Conteos
- `POST /api/v1/conteos/crear` - Crear conteo
- `POST /api/v1/conteos/asignar` - Asignar conteo
- `PUT /api/v1/conteos/{id}/editar` - Editar conteo
- `PUT /api/v1/conteos/{id}/contestar` - Contestar conteo
- `DELETE /api/v1/conteos/{id}` - Eliminar conteo (solo admin)
- `GET /api/v1/conteos/` - Listar conteos
- `GET /api/v1/conteos/{id}` - Obtener conteo específico

## Roles y Permisos

### Administrador (nivel 1)
- Crear, asignar, editar, contestar y eliminar conteos
- Acceso completo a todas las funcionalidades

### Supervisor (nivel 2)
- Crear, asignar, editar y contestar conteos
- No puede eliminar conteos

### CCA - Centro de Control Analítico (nivel 3)
- Crear, asignar y contestar conteos
- No puede editar ni eliminar conteos

### APP - Auxiliar de Prevención de Pérdida (nivel 4)
- Crear y contestar conteos
- No puede asignar, editar ni eliminar conteos

## Funcionalidades Específicas

### Crear Conteo
- Fecha: Automáticamente fecha actual del sistema
- Estado: Finalizado (Envio = 1) por defecto
- Usuario: El mismo que crea es quien realiza

### Asignar Conteo
- Fecha: Puede ser posterior (no anterior) a la actual
- Estado: Pendiente (Envio = 0)
- Usuario: Se asigna manualmente a otro usuario

### Editar Conteo
- Solo conteos pendientes (Envio = 0)
- Conteos finalizados (Envio = 1) no se pueden editar

### Contestar Conteo
- Solo conteos pendientes (Envio = 0)
- Modifica únicamente existencias físicas
- Cambia estado a finalizado (Envio = 1)

## Base de Datos

El sistema utiliza la base de datos `conteos_scisp` con las siguientes tablas principales:

- `usuarios` - Información de usuarios y roles
- `sucursales` - Catálogo de sucursales
- `catalogo` - Productos disponibles
- `conteo` - Registro de conteos
- `conteodetalles` - Detalles de productos por conteo

## Desarrollo

Para contribuir al proyecto:

1. Crear una rama feature
2. Realizar cambios
3. Ejecutar pruebas
4. Crear pull request

## Soporte

Para soporte técnico, contactar al equipo de desarrollo.
