from fastapi import APIRouter, Depends
from app.api.products.climatic_summary.schema import ClimaticSummaryParams
from sqlalchemy.orm.session import Session
from app.api.products.schema import ProductDataParams
from app.db import get_session
from app.services.climatic_summary import FailedCreatingClimaticSummary, climatic_summary_create
from app.utils.product_data import generateProductData
from app.utils.response import get_error_response, get_success_response


router = APIRouter()


@router.post("/")
def create(
    data_params: ProductDataParams,
    product_params: ClimaticSummaryParams,
    db_session: Session = Depends(get_session),
):
    data = generateProductData(data_params, db_session)

    try:
        return get_success_response(
            result=climatic_summary_create(data, product_params),
            message="Successfully created observation_final.",
        )
    except FailedCreatingClimaticSummary as e:
        return get_error_response(message=str(e))
