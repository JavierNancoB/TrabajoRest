from pydantic import BaseModel
from typing import Dict, Optional, Any

class InfoItem(BaseModel):
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
    strata_code: str
    species_code: str
    gender_code: str