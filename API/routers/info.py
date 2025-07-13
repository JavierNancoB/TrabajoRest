from fastapi import APIRouter
from typing import List
from models.schemas import InfoItem
from responses.standard_responses import standard_404, standard_500, response_200_list_example
from services.info_service import fetch_table_data

router = APIRouter(
    prefix="/v1/info",
    tags=["Información base"]
)

# Ejemplos reutilizables por endpoint

# {
#     "code": "0",
#     "name": "Nobleza Suprema"
# }
# {
#     "code": "HU",
#     "name": "Humana."
# }
# {
#     "code": "M",
#     "name": "Masculino"
# }
# Estos ejemplos se usan para documentar las respuestas de los endpoints

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
    return fetch_table_data("isekai", "genders")
