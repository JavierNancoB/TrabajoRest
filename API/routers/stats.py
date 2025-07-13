"""
router/stats.py

Router que expone endpoints estadísticos sobre los personajes del mundo isekai.

Incluye operaciones para calcular:
- Conteo y porcentaje de personajes que cumplen ciertos filtros
- Estadísticas de edad como mínimo, máximo, promedio y desviación estándar
"""

from fastapi import APIRouter, Query, HTTPException
from services.stats_service import count_and_percentage_by_codes, age_stats_by_codes
from responses.standard_responses import standard_500
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter(
    prefix="/v1/stats",
    tags=["Estadísticas"]
)

class CountPercentageResponse(BaseModel):
    """Modelo de respuesta para el conteo y porcentaje filtrado."""
    count: int
    percentage: float

class AgeStatsResponse(BaseModel):
    """Modelo de respuesta para estadísticas de edad."""
    min_age: float
    max_age: float
    avg_age: float
    stddev_age: float


@router.get(
    "/count", 
    summary="Obtener estadísticas de conteo",
    response_model=CountPercentageResponse,
    responses={
        200: {
            "description": "Respuesta exitosa",
            "content": {
                "application/json": {
                    "example": {
                        "count": 8946,
                        "percentage": 0.008946
                    }
                }
            }
        },
        404: {
            "description": "Código no encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "No se encontró código 'HUMAN' en species"
                    }
                }
            }
        },
        422: {
            "description": "Error de validación de parámetros",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "type": "missing",
                                "loc": ["query", "gender_code"],
                                "msg": "Field required",
                                "input": None
                            }
                        ]
                    }
                }
            }
        },
        500: standard_500,
    }
)
def count_persons_with_filters(
    species_code: str = Query(..., description="Código de especie", example="HU"),
    strata_code: str = Query(..., description="Código de estrato", example="0"),
    gender_code: str = Query(..., description="Código de género", example="F"),
):
    """
    Retorna el número de personajes y el porcentaje respecto al total,
    según los filtros de especie, estrato y género.

    Args:
        species_code (str): Código de la especie (e.g., 'HU').
        strata_code (str): Código del estrato social (e.g., '0').
        gender_code (str): Código del género (e.g., 'F').

    Returns:
        dict: Diccionario con `count` (int) y `percentage` (float).

    Raises:
        HTTPException: Si alguno de los códigos no existe (404).
    """
    try:
        result = count_and_percentage_by_codes(
            strata_code=strata_code,
            species_code=species_code,
            gender_code=gender_code
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return result


@router.get(
    "/age", 
    summary="Obtener estadísticas de edad",
    response_model=AgeStatsResponse,
    responses={
        200: {
            "description": "Respuesta exitosa",
            "content": {
                "application/json": {
                    "example": {   
                        "min_age": 0.03,
                        "max_age": 90.01,
                        "avg_age": 45.24,
                        "stddev_age": 26.15
                    }
                }
            }
        },
        404: {
            "description": "Código no encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "No se encontró código 'HUM' en species"
                    }
                }
            }
        },
        422: {
            "description": "Error de validación de parámetros",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "type": "missing",
                                "loc": ["query", "gender_code"],
                                "msg": "Field required",
                                "input": None
                            }
                        ]
                    }
                }
            }
        },
        500: standard_500,
    }
)
def age_stats(
    species_code: str = Query(..., description="Código de especie", example="HU"),
    strata_code: str = Query(..., description="Código de estrato", example="5"),
    gender_code: str = Query(..., description="Código de género", example="M"),
):
    """
    Retorna estadísticas de edad (mínima, máxima, promedio y desviación estándar)
    para los personajes que cumplen con los filtros.

    Args:
        species_code (str): Código de especie (e.g., 'HU').
        strata_code (str): Código de estrato (e.g., '5').
        gender_code (str): Código de género (e.g., 'M').

    Returns:
        dict: Diccionario con `min_age`, `max_age`, `avg_age`, `stddev_age`.

    Raises:
        HTTPException: Si alguno de los códigos no existe (404).
    """
    try:
        result = age_stats_by_codes(
            strata_code=strata_code,
            species_code=species_code,
            gender_code=gender_code
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return result
