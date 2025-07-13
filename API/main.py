from fastapi import FastAPI
from routers import info, stats  # 👈 ahora incluye stats también

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

app = FastAPI(
    title="Un API de otro mundo",
    version="v1",
    description="Documentación de la API del trabajo isekai (simulado) como parte de la asignatura Computación Paralela y Distribuida de la UTEM semestre de otoño 2025.",
    openapi_tags=tags_metadata
)

# Routers
app.include_router(info.router)
app.include_router(stats.router)  # 👈 activar cuando exista
