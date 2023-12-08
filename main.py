import asyncio
import os
from pathlib import Path

from apicall import batch_process
from matrix import build_matrix

base_dir = Path(__file__).resolve().parent
output_dir = base_dir / 'output'
map_chunk = base_dir / 'example.osm'

# Example: https://overpass-api.de/api/map?bbox=138.9001,35.0604,141.0562,36.1157
# Define the boundaries of latitude and longitude
lat_min, lat_max = 35.0604, 36.1157
long_min, long_max = 138.9001, 141.0562

# Define the size of each cell in degrees
cell_size = 0.04


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def build_api_url(left, bottom, right, top):
    """
    Build Overpass API URL using the bounding box parameters.

    :param left: float
        The longitude of the left boundary.
    :param bottom: float
        The latitude of the bottom boundary.
    :param right: float
        The longitude of the right boundary.
    :param top: float
        The latitude of the top boundary.
    :return: str
        The formatted Overpass API URL string.

    # Usage:
    url = build_api_url(138.9001, 35.0604, 141.0562, 36.1157)

    """
    return 'http://overpass-api.de/api/map?bbox={:0.4f},{:0.4f},{:0.4f},{:0.4f}'.format(left, bottom, right, top)


async def main():
    output_dir.mkdir(exist_ok=True)
    urls = []
    matrix = build_matrix(lat_min, lat_max, long_min, long_max, cell_size)

    for row in matrix:
        for cell in row:
            url = build_api_url(cell.long_min, cell.lat_min, cell.long_max, cell.lat_max)
            urls.append(url)

    await batch_process(urls, output_dir)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
