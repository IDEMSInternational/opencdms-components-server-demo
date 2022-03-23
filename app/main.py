from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

# Routers
from app.api.products.climatic_summary.router import router as climatic_summary_router
from app.api.products.inventory_plot.router import router as inventory_plot_router
from app.api.products.inventory_table.router import router as inventory_table_router
from app.api.products.timeseries_plot.router import router as timeseries_plot_router
from app.api.products.test.router import router as test_router


def get_app():
    app = FastAPI(
        title="OpenCDMS Components Api",
        version="1.0.0",
        docs_url="/"
    )

    # Development - include middleware to allow cross-origin-requests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(climatic_summary_router,
                       prefix="/v1/products/climatic-summary", tags=["Climatic Summary"])

    app.include_router(inventory_plot_router,
                       prefix="/v1/products/inventory-plot", tags=["Inventory Plot"])

    app.include_router(inventory_table_router,
                       prefix="/v1/products/inventory-table", tags=["Inventory Table"])

    app.include_router(timeseries_plot_router,
                       prefix="/v1/products/timeseries-plot", tags=["Timeseries Plot"])

    app.include_router(test_router,
                       prefix="/v0/products/test", tags=["Test Functions"])

    # Static file hosting
    app.mount("/outputs", StaticFiles(directory="outputs",
              check_dir=True), name="outputs")

    return app


app = get_app()


# needed for debugging, see https://fastapi.tiangolo.com/tutorial/debugging/
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
