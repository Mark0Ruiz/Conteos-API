from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import conteos, auth
from app.core.database import engine
from app.models import models

# Crear las tablas si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Conteos SCISP",
    description="API para el sistema de conteos de productos en sucursales",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(conteos.router, prefix="/api/v1/conteos", tags=["Conteos"])

@app.get("/")
async def root():
    return {"message": "API Conteos SCISP - Sistema de conteos de productos"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
