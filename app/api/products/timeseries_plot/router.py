from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm.session import Session
from app.api.products.schema import ProductDataParams
from app.api.products.timeseries_plot.schema import TimeseriesPlotParams
from app.db import get_session
from app.services.timeseries_plot import timeseries_plot_create
from app.utils.product_data import generateProductData


router = APIRouter()


@ router.post("/", response_class=FileResponse)
def create(
    data_params: ProductDataParams,
    product_params: TimeseriesPlotParams,
    db_session: Session = Depends(get_session),
):
    data = generateProductData(data_params, db_session)
    outputPath = timeseries_plot_create(data, product_params)
    return FileResponse(outputPath)
