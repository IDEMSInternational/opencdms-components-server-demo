import os
from pandas import DataFrame
from app.api.products.timeseries_plot.schema import TimeseriesPlotParams
from app.utils.product_data import TMP_DIR
from rinstat import cdms_products


def timeseries_plot_create(data: DataFrame, params: TimeseriesPlotParams) -> str:

    output_path: str = TMP_DIR
    output_file_name: str = "timeseries_plot.jpg"

    return_val = cdms_products.timeseries_plot(
        path=output_path,
        file_name=output_file_name,
        data=data,
        date_time=params.date_time,
        elements=params.elements,
        station=params.station,
        facet_by=params.facet_by,
        type=params.type,
        add_points=params.add_points,
        add_line_of_best_fit=params.add_line_of_best_fit,
        se=params.se,
        add_path=params.add_path,
        add_step=params.add_step,
        na_rm=params.na_rm,
        show_legend=params.show_legend,
        title=params.title,
        x_title=params.x_title,
        y_title=params.y_title,
    )

    return_path: str = os.path.join(output_path, output_file_name)
    return return_path
