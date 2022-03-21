from typing import List
from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        extra = "forbid"
        allow_population_by_field_name = True


class Response(BaseSchema):
    message: str
    status: str


class ProductDataParams(BaseModel):
    station_ids: List[int] = [67774010]
    period: List[str] = ['1900-01-01', '2022-01-01']
    elements: List[int] = [3, 4]
