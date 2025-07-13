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
    count: int
    percentage: float

class AgeStatsResponse(BaseModel):
    min_age: int
    max_age: int
    avg_age: float
    count: int


@router.get(
    "/count", 
    summary="Obtener estadisticas de conteo",
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
    Retorna la cantidad y porcentaje de individuos para los filtros dados.
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
                        "min_age": 0,
                        "max_age": 120,
                        "avg_age": 59.76,
                        "count": 8946
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
        strata_code: str = Query(..., description="Código de estrato", example="0"),
        gender_code: str = Query(..., description="Código de género", example="F"),
    ):
    """
    Retorna el valor mínimo, máximo y promedio de edad para los filtros dados.
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