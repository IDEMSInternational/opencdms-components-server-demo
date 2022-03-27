from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm.session import Session
from app.api.products.schema import FileResponseType, ProductDataParams
from app.api.products.inventory_plot.schema import InventoryPlotParams
from app.db import get_session
from app.services.inventory_plot import inventory_plot_create
from app.utils.product_data import generateProductData
from app.utils.response import get_error_response, get_file_response


router = APIRouter()


@router.post("/", response_class=FileResponse)
def create(
    data_params: ProductDataParams,
    product_params: InventoryPlotParams,
    response_type: FileResponseType,
    request: Request,
    db_session: Session = Depends(get_session)
):
    try:
        data = generateProductData(data_params, db_session)
        if data.empty:
            return JSONResponse(content=get_error_response(message="Error - No data exists for query"), status_code=404)
        outputPath = inventory_plot_create(data, product_params)
        return get_file_response(filepath=outputPath, request=request, option=response_type)
    # exception handlers
    except Exception as e:
        return JSONResponse(content=get_error_response(message=str(e)), status_code=400)
