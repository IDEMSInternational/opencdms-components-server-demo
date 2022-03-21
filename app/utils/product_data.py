import os
from pathlib import Path
from pandas import DataFrame, read_csv
from datetime import datetime
from opencdms.models.climsoft import v4_1_1_core as climsoft
from sqlalchemy.orm.session import Session

from app.api.products.schema import ProductDataParams


WORKING_DIR = os.path.dirname(__file__)
ROOT_DIR = Path(WORKING_DIR).parent
MOCK_DATA_DIR = os.path.join(ROOT_DIR, "test")
TMP_DIR = os.path.join(ROOT_DIR, "tmp")

if not os.path.exists(TMP_DIR):
    os.mkdir(TMP_DIR)


def generateProductData(data_params: ProductDataParams, db_session: Session) -> DataFrame:
    # Run queries against climsoft Observation final table
    obs = climsoft.Observationfinal

    # Create date object in given time format yyyy-mm-dd for use in filters
    period_start_date = datetime.strptime(data_params.period[0], "%Y-%m-%d")
    period_end_date = datetime.strptime(data_params.period[1], "%Y-%m-%d")

    print(period_start_date, period_end_date)

    data = (
        db_session.query(obs)
        # https://stackoverflow.com/questions/2128505/difference-between-filter-and-filter-by-in-sqlalchemy
        .filter(obs.recordedFrom.in_(data_params.station_ids))
        .filter(obs.obsDatetime.between(period_start_date, period_end_date))
        .filter(obs.describedBy.in_(data_params.elements))

        # TODO - handle any required data merging
        # .options(joinedload("obselement"), joinedload("station"))

        .limit(100)  # Testing purposes to avoid large calls
        .all()
    )

    return data


def generateProductDataFromCSV() -> DataFrame:
    data_file: str = os.path.join(MOCK_DATA_DIR, "data.csv")
    data = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )
    return data
