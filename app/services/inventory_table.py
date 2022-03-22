from pandas import DataFrame
from app.api.products.inventory_table.schema import InventoryTableParams
from rinstat import cdms_products


def inventory_table_create(data: DataFrame, params: InventoryTableParams) -> str:

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
