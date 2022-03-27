from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.api.products.climatic_summary.schema import ClimaticSummaryParams
from sqlalchemy.orm.session import Session
from app.api.products.schema import DataFrameResponseType, ProductDataParams
from app.db import get_session
from app.services.climatic_summary import climatic_summary_create
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
    try:
        data = generateProductData(data_params, db_session)
        if data.empty:
            return JSONResponse(content=get_error_response(message="Error - No data exists for query"), status_code=404)
        df = climatic_summary_create(data, product_params)
        response = get_dataframe_response(dataframe=df, option=response_type)
        return get_success_response(
            result=response,
            message="Successfully created observation_final.",
        )
    # exception handlers
    except Exception as e:
        return JSONResponse(content=get_error_response(message=str(e)), status_code=400)
