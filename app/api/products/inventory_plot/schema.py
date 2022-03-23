from typing import Dict, List

from pydantic import BaseModel


class InventoryPlotParams(BaseModel):
    date_time: str = 'obsDatetime'
    elements: str = 'obsValue'
    station: str = 'recordedFrom'
    year: str = None
    doy: str = None
    year_doy_plot: bool = False
    facet_by: str = None
    facet_x_size: int = 7
    facet_y_size: int = 11
    title: str = "Inventory Plot"
    plot_title_size: float = None
    plot_title_hjust: float = 0.5
    x_title: str = None
    y_title: str = None
    x_scale_from: int = None
    x_scale_to: int = None
    x_scale_by: int = None
    y_date_format: str = None
    y_date_scale_by: int = None
    y_date_scale_step: int = 1
    facet_scales: str = "fixed"
    facet_dir: str = "h"
    facet_x_margin: List[float] = None
    facet_y_margin: List[float] = None
    facet_nrow: int = None
    facet_ncol: int = None
    missing_colour: str = "red"
    present_colour: str = "grey"
    missing_label: str = "Missing"
    present_label: str = "Present"
    display_rain_days: bool = False
    rain: str = None
    rain_cats: Dict[str, list] = {
        # TODO was '"breaks": [0, 0.85, float("inf")]' but JSON cannot represent infinity
        "breaks": [0, 0.85, 1e100],
        "labels": ["Dry", "Rain"],
        "key_colours": ["tan3", "blue"],
    }
    coord_flip: bool = False
