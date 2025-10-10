from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Configuración de base de datos
    DATABASE_URL: str = "mysql+pymysql://usuario:password@localhost:3306/conteos_scisp"
    
    # Configuración de autenticación
    SECRET_KEY: str = "tu_clave_secreta_muy_segura_aqui_cambiala"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de la aplicación
    PROJECT_NAME: str = "API Conteos SCISP"
    PROJECT_VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"

settings = Settings()
