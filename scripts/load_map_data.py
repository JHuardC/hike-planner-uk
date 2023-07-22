import os
from typing import TypeVar, Literal
from collections import namedtuple
from src.hikeplanner.settings import PROJECT_PATH, GOOGLE_MAPS_API_KEY
import gpxpy
from gpxpy.gpx import GPX, PointData, GPXTrackPoint
from pandas import DataFrame
import pydeck as dek

os.environ['GOOGLE_MAPS_API_KEY'] = GOOGLE_MAPS_API_KEY

# Namespace
PathData = namedtuple(
    'PathData',
    ['latitude', 'longitude', 'elevation'],
    module = 'hikeplanner'
)

# functions
def yield_gpx_map_points(gpx: GPX) -> list[float]:
    """
    Extracts all map points from GPX object.
    """
    point_data: PointData
    for point_data in gpx.get_points_data(distance_2d = False):
        point = point_data.point
        yield [point.latitude, point.longitude]
        
def generate_path(gpx: GPX) -> dict[Literal['path'], list[list[float]]]:
    """
    Converts gpx file format to a coordinate format usable by Layers
    """
    return {
        'path': [el for el in yield_gpx_map_points(gpx = gpx)],
        'colour': (0, 0, 0)
    }
    

if __name__ == "__main__":
    
    with open(PROJECT_PATH.joinpath('data', 'wessexridgeway.gpx'), 'r') as f:
        data = generate_path(gpxpy.parse(f))

    path_lyr = dek.Layer(
        type = 'PathLayer',
        data = DataFrame([data]),
        get_path = 'path',
        get_color = 'colour',
        get_width=20
    )

    view_state = dek.ViewState(
    latitude = data['path'][-1][0],
    longitude = data['path'][-1][1],
    zoom = 10
    )
    
    deck = dek.Deck(
        layers = [path_lyr],
        initial_view_state = view_state,
        map_provider = 'google_maps',
        map_style = 'roadmap'
    )