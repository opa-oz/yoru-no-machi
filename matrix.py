import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon

from models import Cell


def build_matrix_geopandas(lat_min, lat_max, long_min, long_max, cell_size) -> gpd.GeoDataFrame:
    # Create the latitude and longitude ranges
    lat_range = np.arange(lat_min, lat_max, cell_size)
    long_range = np.arange(long_min, long_max, cell_size)

    # Create a list to hold the polygons
    polygons = []

    # Create the polygons for each cell in the grid
    for lat in lat_range:
        for lon in long_range:
            # Create the points of the polygon
            points = [(lon, lat), (lon + cell_size, lat), (lon + cell_size, lat + cell_size), (lon, lat + cell_size)]
            # Create the polygon and append it to the list
            polygons.append(Polygon(points))

    # Create a GeoDataFrame from the polygons
    gdf = gpd.GeoDataFrame(geometry=polygons)

    return gdf


def build_matrix(lat_min, lat_max, long_min, long_max, cell_size) -> list[list[Cell]]:
    # Create the latitude and longitude ranges
    lat_range = np.arange(lat_min, lat_max, cell_size)
    long_range = np.arange(long_min, long_max, cell_size)

    # Initialize the 2D matrix
    matrix = np.empty((len(lat_range), len(long_range)), dtype=object)

    # Populate the 2D matrix with cells representing chunks of coordinates
    for i, lat in enumerate(lat_range):
        for j, long in enumerate(long_range):
            cell = Cell(
                lat_min=lat,
                lat_max=lat + cell_size,
                long_min=long,
                long_max=long + cell_size
            )
            matrix[i, j] = cell

    return matrix
