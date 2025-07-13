"""
router/info.py

Router que expone endpoints para obtener información base desde el mundo isekai,
como los estratos sociales, especies y géneros disponibles.

Estos datos se usan como filtros en endpoints estadísticos y son estáticos en la base de datos.
"""

from fastapi import APIRouter
from typing import List
from models.schemas import InfoItem
from responses.standard_responses import standard_404, standard_500, response_200_list_example
from services.info_service import fetch_table_data

router = APIRouter(
    prefix="/v1/info",
    tags=["Información base"]
)

# Ejemplos para documentación Swagger
strata_example = [{"code": "0", "name": "Nobleza Suprema"}]
species_example = [{"code": "HU", "name": "Humana."}]
genders_example = [{"code": "M", "name": "Masculino"}]

@router.get(
    "/strata",
    response_model=List[InfoItem],
    summary="Listar estratos sociales disponibles",
    responses={
        200: response_200_list_example("Listado de estratos obtenido exitosamente", strata_example),
        404: standard_404,
        500: standard_500,
    }
)
def get_strata():
    """
    Retorna la lista de estratos sociales definidos en el mundo isekai.

    Returns:
        List[InfoItem]: Lista de objetos con código y nombre del estrato.
    """
    return fetch_table_data("isekai", "strata")


@router.get(
    "/species",
    response_model=List[InfoItem],
    summary="Listar especies disponibles",
    responses={
        200: response_200_list_example("Listado de especies obtenido exitosamente", species_example),
        404: standard_404,
        500: standard_500,
    }
)
def get_species():
    """
    Retorna la lista de especies disponibles en la base de datos.

    Returns:
        List[InfoItem]: Lista de objetos con código y nombre de cada especie.
    """
    return fetch_table_data("isekai", "species")


@router.get(
    "/genders",
    response_model=List[InfoItem],
    summary="Listar géneros disponibles",
    responses={
        200: response_200_list_example("Listado de géneros obtenido exitosamente", genders_example),
        404: standard_404,
        500: standard_500,
    }
)
def get_genders():
    """
    Retorna la lista de géneros registrados en el sistema.

    Returns:
        List[InfoItem]: Lista de objetos con código y nombre del género.
    """
    return fetch_table_data("isekai", "genders")
