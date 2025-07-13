from models.schemas import ProblemDetails
from typing import Dict

standard_404 = {
    "model": ProblemDetails,
    "description": "No hay información disponible",
    "content": {
        "application/problem+json": {
            "example": {
                "type": "https://example.com/",
                "title": "Recurso no encontrado",
                "status": 404,
                "detail": "No hay información disponible",
                "instance": "https://example.com/",
                "properties": {
                    "additionalProp1": "string",
                    "additionalProp2": "string",
                    "additionalProp3": "string"
                }
            }
        }
    }
}

standard_500 = {
    "model": ProblemDetails,
    "description": "Error interno no manejado",
    "content": {
        "application/problem+json": {
            "example": {
                "type": "https://example.com/",
                "title": "Error interno",
                "status": 500,
                "detail": "Error inesperado en el servidor",
                "instance": "https://example.com/",
                "properties": {
                    "additionalProp1": "string",
                    "additionalProp2": "string",
                    "additionalProp3": "string"
                }
            }
        }
    }
}

def response_200_list_example(description: str, example_list: list) -> Dict:
    return {
        "description": description,
        "content": {
            "application/json": {
                "example": example_list
            }
        }
    }
