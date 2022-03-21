from pydantic import BaseModel


class TimeseriesPlotParams(BaseModel):
    date_time: str
    elements: str
    station: str = None
    facet_by: str = "stations"
    type: str = "line"
    add_points: bool = False
    add_line_of_best_fit: bool = False
    se: bool = True
    add_path: bool = False
    add_step: bool = False
    na_rm: bool = False
    show_legend: bool = None  # Convert None to R NA
    title: str = "Timeseries Plot"
    x_title: str = None
    y_title: str = None
