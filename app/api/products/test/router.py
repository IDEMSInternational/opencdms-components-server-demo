
import base64
import json
import os
import shutil
from types import SimpleNamespace
from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse
from pydantic import Json
from sqlalchemy.orm.session import Session
from app.api.products.schema import ImageLinkResponse, ProductDataParams
from app.db import get_session
from app.utils.product_data import ROOT_DIR, generateProductData, generateProductDataFromCSV, MOCK_DATA_DIR
from app.services.timeseries_plot import timeseries_plot_create
from app.utils.response import get_file_link_response, get_file_response


router = APIRouter()


@ router.post("/data_test")
def test_data_api(data_params: ProductDataParams, db_session: Session = Depends(get_session)) -> Json:
    data = generateProductData(data_params, db_session)
    return json.loads(data.to_json(orient='records'))


@ router.post("/image_test", response_class=FileResponse)
# Generate a timeseries_plot image and return as a FileResponse
def image_test() -> FileResponse:
    # Use test csv data
    data = generateProductDataFromCSV()
    # Use test timeseries_plot input data, mapping key-value pairs as tuple for function params
    inputJson = os.path.join(MOCK_DATA_DIR, "timeseries_plot.input.json")
    with open(inputJson) as f:
        params = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
        outputPath = timeseries_plot_create(data, params)
        return FileResponse(outputPath)


@ router.post("/image_test_file", response_class=FileResponse)
# Return an image as a FileResponse (buffer stream)
def image_test_file(request: Request) -> FileResponse:
    imgPath = os.path.join(MOCK_DATA_DIR, "inventory_plot.output.jpeg")
    return get_file_response(filepath=imgPath, request=request, option='file')


@ router.post("/image_test_b64")
# Return an image encoded in base64
def image_test_base64(request: Request) -> str:
    imgPath = os.path.join(MOCK_DATA_DIR, "inventory_plot.output.jpeg")
    return get_file_response(filepath=imgPath, request=request, option='base64')


@ router.post("/image_test_link", response_model=ImageLinkResponse)
# Copy a test image to static output dir and return direct download link
def image_test_b64(request: Request):
    imgPath = os.path.join(MOCK_DATA_DIR, "inventory_plot.output.jpeg")
    return get_file_response(filepath=imgPath, request=request, option='link')
