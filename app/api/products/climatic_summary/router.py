from fastapi import APIRouter, Depends
from app.api.products.climatic_summary.schema import ClimaticSummaryParams
from app.utils.response import get_success_response
from climsoft_api.services import observationfinal_service
import climsoft_api.api.observationfinal.schema as observationfinal_schema
from sqlalchemy.orm.session import Session
from climsoft_api.api import deps


router = APIRouter()


@router.post(
    "/",
    # response_model=observationfinal_schema.ObservationFinalResponse,
)
def create_climatic_summary(
    data_params,
    product_params: ClimaticSummaryParams,
    db_session: Session = Depends(deps.get_session),
):
    try:

        return get_success_response(
            result=[observationfinal_service.create(
                db_session=db_session, data=data)],
            message="Successfully created observation_final.",
        )
    except observationfinal_service.FailedCreatingObservationFinal as e:
        return get_error_response(message=str(e))
