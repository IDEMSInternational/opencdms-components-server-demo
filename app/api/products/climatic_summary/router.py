from fastapi import APIRouter, Depends
from app.api.products.climatic_summary.schema import ClimaticSummaryParams
from sqlalchemy.orm.session import Session
from app.api.products.schema import DataFrameResponseType, ProductDataParams
from app.db import get_session
from app.services.climatic_summary import FailedCreatingClimaticSummary, climatic_summary_create
from app.utils.product_data import generateProductData
from app.utils.response import get_error_response, get_success_response, get_dataframe_response


router = APIRouter()


@router.post("/")
def create(
    data_params: ProductDataParams,
    product_params: ClimaticSummaryParams,
    response_type: DataFrameResponseType = DataFrameResponseType.records,
    db_session: Session = Depends(get_session),
):
    data = generateProductData(data_params, db_session)

    try:
        df = climatic_summary_create(data, product_params)
        response = get_dataframe_response(dataframe=df, option=response_type)
        return get_success_response(
            result=response,
            message="Successfully created observation_final.",
        )
    except FailedCreatingClimaticSummary as e:
        return get_error_response(message=str(e))
