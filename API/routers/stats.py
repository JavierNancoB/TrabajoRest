from fastapi import APIRouter, Query, HTTPException
from services.stats_service import count_and_percentage_by_codes
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

@router.get(
    "/count", 
    summary="Contar personas filtradas y porcentaje",
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
def count_persons_with_filters(
        strata_code: str = Query(..., description="Código de estrato", example="0"),
        species_code: str = Query(..., description="Código de especie", example="HU"),
        gender_code: str = Query(..., description="Código de género", example="F"),
    ):
    """
    Retorna cuántas personas cumplen con los filtros dados y su porcentaje respecto al total.
    Lanza 404 si alguno de los códigos no existe.
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
