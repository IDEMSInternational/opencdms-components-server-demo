import os
from pandas import DataFrame, read_csv
from app.main import MOCK_DATA_DIR


def generateProductData() -> DataFrame:
    data_file: str = os.path.join(MOCK_DATA_DIR, "data.csv")
    data = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )
    return data
