"""
Loads Key Constants used by Hike Planner UK Project.
"""
import os
from typing import Final
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Google Maps API key
with open(Path(os.getenv('MAPS_API_KEY_PATH')), 'r') as f:
    GOOGLE_MAPS_API: Final[str] = f.read()

# Project Path
PROJECT_PATH: Final[Path] = Path(os.getenv('PROJECT_DIR'))

if __name__ == "__main__":
    print(f'{PROJECT_PATH = }', f'{GOOGLE_MAPS_API =}', sep = '\n')