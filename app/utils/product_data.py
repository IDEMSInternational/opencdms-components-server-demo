import os
from pathlib import Path
from fastapi import Query
from pandas import DataFrame, read_csv, read_sql
from datetime import datetime
from opencdms.models.climsoft import v4_1_1_core as climsoft
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.query import Query as SqlQuery

from app.api.products.schema import ProductDataParams


WORKING_DIR = os.path.dirname(__file__)
ROOT_DIR = Path(WORKING_DIR).parent.parent
MOCK_DATA_DIR = os.path.join(ROOT_DIR, "test")
TMP_DIR = os.path.join(ROOT_DIR, "tmp")

if not os.path.exists(TMP_DIR):
    os.mkdir(TMP_DIR)


def generateProductData(
    data_params: ProductDataParams, db_session: Session
) -> DataFrame:
    # Run queries against climsoft Observation final table
    obs = climsoft.Observationfinal

    # Create date object in given time format yyyy-mm-dd for use in filters
    period_start_date = datetime.strptime(data_params.period[0], "%Y-%m-%d")
    period_end_date = datetime.strptime(data_params.period[1], "%Y-%m-%d")

    print(period_start_date, period_end_date)

    """data = (
        db_session.query(obs)
        .filter(obs.recordedFrom.in_(data_params.station_ids))
        .filter(obs.obsDatetime.between(period_start_date, period_end_date))
        .filter(obs.describedBy.in_(data_params.elements))
        .all()
    )"""
    query: SqlQuery = (
        db_session.query(obs)
        .filter(obs.recordedFrom.in_(data_params.station_ids))
        .filter(obs.obsDatetime.between(period_start_date, period_end_date))
        .filter(obs.describedBy.in_(data_params.elements))
    )

    df: DataFrame = read_sql(query.statement, db_session.get_bind())
    return df


def generateProductDataFromCSV() -> DataFrame:
    data_file: str = os.path.join(MOCK_DATA_DIR, "data.csv")
    data = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )
    return data
