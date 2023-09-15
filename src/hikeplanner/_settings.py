"""
Loads Key Constants used by Hike Planner UK Project.
"""
from pathlib import Path
import yaml

with open(Path(__file__).absolute().parent.joinpath('config.yaml'), 'r') as f:
    presets: dict[str, dict[str, str | int] | str | int] = yaml.safe_load(f)


if __name__ == '__main__':
    print(presets)