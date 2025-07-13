from fastapi import FastAPI
from routers import info, stats  # 👈 ahora incluye stats también

# Metadata para los tags usados en la documentación OpenAPI
tags_metadata = [
    {
        "name": "Información base",
        "description": "Proporciona listas de especies, estratos sociales y géneros"
    },
    {
        "name": "Estadísticas",
        "description": "Endpoints para obtener estadísticas de edad y conteo"
    }
]

# Crear la instancia principal de la aplicación FastAPI
app = FastAPI(
    title="Un API de otro mundo",
    version="v1",
    description=(
        "Documentación de la API del trabajo isekai (simulado) como parte de la "
        "asignatura Computación Paralela y Distribuida de la UTEM semestre de otoño 2025."
    ),
    openapi_tags=tags_metadata
)
"""
Instancia principal de la aplicación FastAPI.

Esta API proporciona información básica y estadísticas de personajes de un mundo ficticio.
Está diseñada como parte de un proyecto universitario para demostrar conceptos de
programación paralela y distribuida usando FastAPI.

Attributes:
    app (FastAPI): Aplicación principal que sirve todos los endpoints definidos en los routers.
"""

# Incluir los routers que manejan los distintos endpoints
app.include_router(info.router)
"""
Incluye el router `info`, que proporciona endpoints para obtener listas de especies,
estratos sociales y géneros disponibles en el sistema.
"""

app.include_router(stats.router)  # 👈 activar cuando exista
"""
Incluye el router `stats`, que proporciona endpoints para calcular estadísticas
de edad y conteo por distintas combinaciones de filtros.

Este router aprovecha la paralelización de consultas SQL para mejorar el rendimiento.
"""
