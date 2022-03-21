from datetime import datetime
import importlib
import os
from base64 import b64decode
from cmath import nan
from pathlib import Path
from typing import Dict, List, Optional
from uuid import uuid4

import uvicorn  # needed for debugging, see https://fastapi.tiangolo.com/tutorial/debugging/
from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse
from pandas import DataFrame, read_csv
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.db import get_session

from opencdms.models.climsoft import v4_1_1_core as climsoft

from rinstat import cdms_products

WORKING_DIR = os.path.dirname(__file__)
ROOT_DIR = Path(WORKING_DIR).parent
MOCK_DATA_DIR = os.path.join(ROOT_DIR, "test")
TMP_DIR = os.path.join(ROOT_DIR, "tmp")

if not os.path.exists(TMP_DIR):
    os.mkdir(TMP_DIR)


class ClimaticSummaryParams(BaseModel):
    data: str
    date_time: str
    station: str = None
    elements: List = []
    year: str = None
    month: str = None
    dekad: str = None  # TODO add type
    pentad: str = None  # TODO add type
    to: str = "hourly"
    by: str = None  # TODO add type
    doy: str = None
    doy_first: int = 1
    doy_last: int = 366
    summaries: Dict = {"n": "dplyr::n"}
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


class InventoryTableParams(BaseModel):
    data: str
    date_time: str
    elements: List
    station: str = None
    year: str = None
    month: str = None
    day: str = None
    missing_indicator: str = "M"
    observed_indicator: str = "X"


class TimeseriesPlotParams(BaseModel):
    data: str
    date_time: str
    elements: str
    station: str = None
    facet_by: str = "stations"
    type: str = "line"
    add_points: bool = False
    add_line_of_best_fit: bool = False
    se: bool = True
    add_path: bool = False
    add_step: bool = False
    na_rm: bool = False
    show_legend: bool = None  # Convert None to R NA
    title: str = "Timeseries Plot"
    x_title: str = None
    y_title: str = None


app = FastAPI(
    title="OpenCDMS Components Api",
    version="1.0.0",
)


@ app.post("/test_data_api")
# Inject the session from generator
def test_data_api(db_session: Session = Depends(get_session)) -> str:

    filters = {
        "station_id": '67774010',
        "period_start": '1991-01-01',
        "period_end": '1991-01-10',

        # TODO - handle filtering by element
        # "elements": ["wind_speed", "wind_direction"],
    }

    # Run queries against climsoft Observation final table
    obs = climsoft.Observationfinal

    # Create date object in given time format yyyy-mm-dd for use in filters
    period_start_date = datetime.strptime(filters['period_start'], "%Y-%m-%d")
    period_end_date = datetime.strptime(filters['period_end'], "%Y-%m-%d")

    data = (
        db_session.query(obs)
        # https://stackoverflow.com/questions/2128505/difference-between-filter-and-filter-by-in-sqlalchemy
        .filter_by(recordedFrom=filters["station_id"])
        .filter(obs.obsDatetime >= period_start_date)
        .filter(obs.obsDatetime <= period_end_date)

        # TODO - handle any required data merging
        # .options(joinedload("obselement"), joinedload("station"))

        .limit(100)  # Testing purposes to avoid large calls
        .all()
    )

    return data


@ app.post("/climatic_summary")
def climatic_summary(params: ClimaticSummaryParams) -> str:

    data_file: str = os.path.join(MOCK_DATA_DIR, "data.csv")
    data = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    df = cdms_products.climatic_summary(
        data=data,
        date_time=params.date_time,
        station=params.station,
        elements=params.elements,
        year=params.year,
        month=params.month,
        dekad=params.dekad,
        pentad=params.pentad,
        to=params.to,
        by=params.by,
        doy=params.doy,
        doy_first=params.doy_first,
        doy_last=params.doy_last,
        summaries=params.summaries,
        na_rm=params.na_rm,
        na_prop=params.na_prop,
        na_n=params.na_n,
        na_consec=params.na_consec,
        na_n_non=params.na_n_non,
        first_date=params.first_date,
        n_dates=params.n_dates,
        last_date=params.last_date,
        summaries_params=params.summaries_params,
        names=params.names,
    )

    df_json: str = df.to_json()
    return df_json


@ app.post("/inventory_table")
def inventory_table(params: InventoryTableParams) -> str:

    data_file: str = os.path.join(MOCK_DATA_DIR, "data.csv")
    data = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    df = cdms_products.inventory_table(
        data=data,
        date_time=params.date_time,
        elements=params.elements,
        station=params.station,
        year=params.year,
        month=params.month,
        day=params.day,
        missing_indicator=params.missing_indicator,
        observed_indicator=params.observed_indicator,
    )

    df_json: str = df.to_json()
    return df_json


@ app.post("/timeseries_plot", response_class=FileResponse)
def timeseries_plot(params: TimeseriesPlotParams) -> str:

    data_file: str = os.path.join(MOCK_DATA_DIR, "data.csv")
    data = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    output_path: str = TMP_DIR
    output_file_name: str = "timeseries_plot.jpg"

    return_val = cdms_products.timeseries_plot(
        path=output_path,
        file_name=output_file_name,
        data=data,
        date_time=params.date_time,
        elements=params.elements,
        station=params.station,
        facet_by=params.facet_by,
        type=params.type,
        add_points=params.add_points,
        add_line_of_best_fit=params.add_line_of_best_fit,
        se=params.se,
        add_path=params.add_path,
        add_step=params.add_step,
        na_rm=params.na_rm,
        show_legend=params.show_legend,
        title=params.title,
        x_title=params.x_title,
        y_title=params.y_title,
    )

    return_path: str = os.path.join(output_path, output_file_name)
    return FileResponse(return_path)


@ app.get("/")
def status_check():
    return {"Status": "Running"}


@ app.get("/exec")
# Test execution of base-64 encoded python code with sample string
def exec_test():
    # Function as string to be executed (converted via https://www.base64decode.org/ )
    code_b64 = "ZGVmIG1haW4oKToKICAgIHJldHVybiAiVGVzdCBzdWNjZXNzZnVsIg=="
    res = exec_code(code_b64, "main")
    return res


@ app.post("/exec")
# Execute base-64 encoded python code from request
def exec_post(py_code_b64: str, fn_name="main"):
    res = exec_code(py_code_b64, fn_name)
    return res


def exec_code(code_b64: str, fn_name="main"):
    # Decode b64 code, write to file, dynamically import, execute code
    # delete file and return execution result
    task_id = uuid4()
    mod_path = f"app/modules/{task_id}.py"
    code = b64decode(code_b64).decode("utf-8")
    with open(mod_path, "w") as file:
        file.write(code)

    mod = importlib.import_module(f"app.modules.{task_id}")
    if hasattr(mod, fn_name):
        fn = getattr(mod, fn_name)
        res = fn()
        os.remove(mod_path)
        return res


# needed for debugging, see https://fastapi.tiangolo.com/tutorial/debugging/
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# TODO - add fallback if not found

# (alternatives)
# res1 = eval(mycode)
# res2 = exec(mycode)

# Adapted from https://python.hotexamples.com/examples/importlib/-/find_spec/python-find_spec-function-examples.html
