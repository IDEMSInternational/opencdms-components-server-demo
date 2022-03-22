
import json
import os
from types import SimpleNamespace
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from pydantic import Json
from sqlalchemy.orm.session import Session
from app.api.products.schema import ProductDataParams
from app.db import get_session
from app.utils.product_data import generateProductData, generateProductDataFromCSV, MOCK_DATA_DIR
from app.services.timeseries_plot import timeseries_plot_create


router = APIRouter()


@ router.post("/data_test")
def test_data_api(data_params: ProductDataParams, db_session: Session = Depends(get_session)) -> Json:

    data = generateProductData(data_params, db_session)
    return json.loads(data.to_json(orient='records'))


@ router.post("/image_test", response_class=FileResponse)
def test_data_api() -> Json:
    # Use test csv data
    data = generateProductDataFromCSV()
    # Use test timeseries_plot input data, mapping key-value pairs as tuple for function params
    inputJson = os.path.join(MOCK_DATA_DIR, "timeseries_plot.input.json")
    with open(inputJson) as f:
        params = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
        outputPath = timeseries_plot_create(data, params)
        return FileResponse(outputPath)
