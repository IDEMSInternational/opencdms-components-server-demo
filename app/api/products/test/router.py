import json
import os
from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse
from pydantic import Json
from sqlalchemy.orm.session import Session
from app.api.products.schema import FileResponseType, ImageLinkResponse, ProductDataParams
from app.db import get_session
from app.utils.paths import MOCK_DATA_DIR
from app.utils.product_data import generateProductData
from app.utils.response import get_file_response


router = APIRouter()


@ router.post("/data_test")
def test_data_api(data_params: ProductDataParams, db_session: Session = Depends(get_session)) -> Json:
    data = generateProductData(data_params, db_session)
    return json.loads(data.to_json(orient='records'))


@ router.post("/image_test")
# Generate a timeseries_plot image and return as a FileResponse
def image_test(response_type: FileResponseType, request: Request):
    imgPath = os.path.join(MOCK_DATA_DIR, "inventory_plot.output.jpeg")
    return get_file_response(filepath=imgPath, request=request, option=response_type)


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
