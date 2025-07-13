"""
standard_responses.py

Respuestas estandarizadas reutilizables para los endpoints de la API.

Incluye formatos consistentes para errores comunes (404, 500) y una función
para generar respuestas exitosas personalizadas con ejemplos.
"""

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
"""Respuesta estándar para errores 404 (no encontrado)."""

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
"""Respuesta estándar para errores 500 (error interno del servidor)."""

def response_200_list_example(description: str, example_list: list) -> Dict:
    """
    Genera una respuesta de ejemplo exitosa (200 OK) con una lista como contenido.

    Args:
        description (str): Descripción de la respuesta.
        example_list (list): Lista de objetos de ejemplo a incluir en la documentación.

    Returns:
        Dict: Estructura compatible con OpenAPI para documentación personalizada.
    """
    return {
        "description": description,
        "content": {
            "application/json": {
                "example": example_list
            }
        }
    }
