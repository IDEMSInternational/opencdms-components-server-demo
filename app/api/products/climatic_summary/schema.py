from typing import Dict, List
from pydantic import BaseModel


class ClimaticSummaryParams(BaseModel):
    date_time: str = "obsDatetime"
    station: str = "recordedFrom"
    elements: List = ["obsValue"]
    year: str = None
    month: str = None
    dekad: str = None  # TODO add type
    pentad: str = None  # TODO add type
    to: str = "hourly"
    by: str = None  # TODO add type
    doy: str = None
    doy_first: int = 1
    doy_last: int = 366
    summaries: Dict = {
        "mean": "mean",
        "max": "max",
        "min": "min"
    }
    na_rm: bool = False
    na_prop: int = None
    na_n: int = None
    na_consec: int = None
    na_n_non: int = None
    first_date: bool = False
    n_dates: bool = False
    last_date: bool = False
    summaries_params: List = []
    names: str = "{.fn}_{.col}"
