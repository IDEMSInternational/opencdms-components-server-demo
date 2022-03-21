from fastapi import APIRouter, Depends
from pandas import read_csv
from app.api.products.climatic_summary.schema import ClimaticSummaryParams
from sqlalchemy.orm.session import Session
from app.api.products.inventory_table.schema import InventoryTableParams
from app.db import get_session
from app.services.inventory_table import inventory_table_create
from app.utils.product_data import generateProductData

router = APIRouter()


@ router.post("/")
def create(
    data_params,
    product_params: ClimaticSummaryParams,
    db_session: Session = Depends(get_session),
):
    data = generateProductData(data_params, db_session)
    inventory_table_create(data, product_params)
