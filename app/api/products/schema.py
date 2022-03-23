from enum import Enum
from typing import List
from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        extra = "forbid"
        allow_population_by_field_name = True


class Response(BaseSchema):
    message: str
    status: str


class FileResponseOptions(Enum):
    file = 'file'
    base64 = 'base64'


class ProductDataParams(BaseModel):
    station_ids: List[int] = [67774010, 67963040]
    period: List[str] = ['2000-01-01', '2000-03-01']
    elements: List[int] = [2, 4]


class ImageLinkResponse(BaseModel):
    link: str
