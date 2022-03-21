from app.api.products.climatic_summary.schema import ClimaticSummaryParams
from rinstat import cdms_products


def create(data, params: ClimaticSummaryParams) -> str:

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
