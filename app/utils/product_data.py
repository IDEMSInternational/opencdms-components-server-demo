import os

from pandas import DataFrame, read_csv, read_sql
from datetime import datetime
from opencdms.models.climsoft import v4_1_1_core as climsoft
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.query import Query as SqlQuery

from app.api.products.schema import ProductDataParams
from app.utils.paths import MOCK_DATA_DIR


def generateProductData(
    data_params: ProductDataParams, db_session: Session
) -> DataFrame:
    # Run queries against climsoft Observation final table
    obs = climsoft.Observationfinal

    # Create date object in given time format yyyy-mm-dd for use in filters
    period_start_date = datetime.strptime(data_params.period[0], "%Y-%m-%d")
    period_end_date = datetime.strptime(data_params.period[1], "%Y-%m-%d")

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
