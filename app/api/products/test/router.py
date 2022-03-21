
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from app.api.products.schema import ProductDataParams
from app.db import get_session
from app.utils.product_data import generateProductData


router = APIRouter()


@ router.post("/data_api")
# Inject the session from generator
def test_data_api(data_params: ProductDataParams, db_session: Session = Depends(get_session)) -> str:

    print("Generate test data", data_params)
    data = generateProductData(data_params, db_session)
    return data
