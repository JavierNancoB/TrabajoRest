"""
schemas.py

Modelos Pydantic utilizados en la API para validar entradas y salidas.

Incluye estructuras reutilizables como `InfoItem` y `ProblemDetails`.
"""

from pydantic import BaseModel
from typing import Dict, Optional, Any

class InfoItem(BaseModel):
    """
    Representa un ítem de información base como especie, género o estrato social.

    Attributes:
        code (str): Código identificador del ítem.
        name (str): Nombre descriptivo del ítem.
    """
    code: str
    name: str

    class Config:
        schema_extra = {
            "example": {
                "code": "001",
                "name": "Chile"
            }
        }

class ProblemDetails(BaseModel):
    """
    Modelo basado en RFC 7807 para describir errores de forma estructurada.

    Attributes:
        type (str): URI que identifica el tipo de error.
        title (str): Título corto del problema.
        status (int): Código HTTP correspondiente.
        detail (str): Descripción detallada del problema.
        instance (str): URI que identifica esta ocurrencia específica del problema.
        properties (dict): Información adicional (extensiones personalizadas).
    """
    type: Optional[str] = "https://example.com/"
    title: Optional[str] = "string"
    status: int = 0
    detail: Optional[str] = "string"
    instance: Optional[str] = "https://example.com/"
    properties: Optional[Dict[str, Any]] = {
        "additionalProp1": "string",
        "additionalProp2": "string",
        "additionalProp3": "string"
    }

class CountFilterInput(BaseModel):
    """
    Modelo de entrada para filtros usados en endpoints estadísticos.

    Attributes:
        strata_code (str): Código del estrato social.
        species_code (str): Código de especie.
        gender_code (str): Código de género.
    """
    strata_code: str
    species_code: str
    gender_code: str
