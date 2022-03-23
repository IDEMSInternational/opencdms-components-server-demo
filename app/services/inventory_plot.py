import os
from pandas import DataFrame
from app.api.products.inventory_plot.schema import InventoryPlotParams
from app.utils.paths import TMP_DIR
from rinstat import cdms_products


def inventory_plot_create(data: DataFrame, params: InventoryPlotParams) -> str:

    output_path: str = TMP_DIR
    output_file_name: str = "inventory_plot.jpg"

    return_val = cdms_products.inventory_plot(
        path=output_path,
        file_name=output_file_name,
        data=data,
        date_time=params.date_time,
        elements=params.elements,
        station=params.station,
        year=params.year,
        doy=params.doy,
        year_doy_plot=params.year_doy_plot,
        facet_by=params.facet_by,
        facet_x_size=params.facet_x_size,
        facet_y_size=params.facet_y_size,
        title=params.title,
        plot_title_size=params.plot_title_size,
        plot_title_hjust=params.plot_title_hjust,
        x_title=params.x_title,
        y_title=params.y_title,
        x_scale_from=params.x_scale_from,
        x_scale_to=params.x_scale_to,
        x_scale_by=params.x_scale_by,
        y_date_format=params.y_date_format,
        y_date_scale_by=params.y_date_scale_by,
        y_date_scale_step=params.y_date_scale_step,
        facet_scales=params.facet_scales,
        facet_dir=params.facet_dir,
        facet_x_margin=params.facet_x_margin,
        facet_y_margin=params.facet_y_margin,
        facet_nrow=params.facet_nrow,
        facet_ncol=params.facet_ncol,
        missing_colour=params.missing_colour,
        present_colour=params.present_colour,
        missing_label=params.missing_label,
        present_label=params.present_label,
        display_rain_days=params.display_rain_days,
        rain=params.rain,
        rain_cats=params.rain_cats,
        coord_flip=params.coord_flip,
    )

    return_path: str = os.path.join(output_path, output_file_name)
    return return_path
