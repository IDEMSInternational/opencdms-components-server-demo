from typing import List
from pydantic import BaseModel


class InventoryTableParams(BaseModel):
    date_time: str
    elements: List
    station: str = None
    year: str = None
    month: str = None
    day: str = None
    missing_indicator: str = "M"
    observed_indicator: str = "X"
