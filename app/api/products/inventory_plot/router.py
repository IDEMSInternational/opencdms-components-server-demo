from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm.session import Session
from app.api.products.schema import FileResponseType, ProductDataParams
from app.api.products.inventory_plot.schema import InventoryPlotParams
from app.db import get_session
from app.services.inventory_plot import inventory_plot_create
from app.utils.product_data import generateProductData
from app.utils.response import get_file_response


router = APIRouter()


@router.post("/", response_class=FileResponse)
def create(
    data_params: ProductDataParams,
    product_params: InventoryPlotParams,
    response_type: FileResponseType,
    request: Request,
    db_session: Session = Depends(get_session)
):
    data = generateProductData(data_params, db_session)
    outputPath = inventory_plot_create(data, product_params)
    return get_file_response(filepath=outputPath, request=request, option=response_type)
