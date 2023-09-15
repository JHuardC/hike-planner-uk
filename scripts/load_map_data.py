from typing import Final
from pathlib import Path
from typing import Literal
from collections import namedtuple
import gpxpy
from gpxpy.gpx import GPX, PointData, GPXTrackPoint
import pydeck as dek
import dotenv
from src.hikeplanner import presets

dot_env = dotenv.find_dotenv()
PROJECT_PATH: Final[Path] = Path(dotenv.get_key(dot_env, 'PROJECT_DIR'))
with open(Path(dotenv.get_key(dot_env, 'MAPS_API_KEY_PATH'))) as f:
    GOOGLE_MAPS_API_KEY: Final[str] = f.read()

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
        yield [point.longitude, point.latitude]
        
def generate_path(gpx: GPX) -> dict[Literal['path'], list[list[float]]]:
    """
    Converts gpx file format to a coordinate format usable by Layers
    """
    return [{
        'path': [el for el in yield_gpx_map_points(gpx = gpx)],
        'colour': (0, 0, 0)
    }]
    

if __name__ == "__main__":
    
    with open(PROJECT_PATH.joinpath('data', 'wessexridgeway.gpx'), 'r') as f:
        data = generate_path(gpxpy.parse(f))

    path_lyr = dek.Layer(
        data = data,
        **presets['layer']
    )

    view_state = dek.ViewState(
    latitude = data[0]['path'][-1][1],
    longitude = data[0]['path'][-1][0],
    zoom = 10
    )
    
    deck = dek.Deck(
        layers = [path_lyr],
        initial_view_state = view_state,
        api_keys = {'google_maps': GOOGLE_MAPS_API_KEY},
        **presets['deck']
    )

    deck