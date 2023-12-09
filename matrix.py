import pickle
from pathlib import Path

import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon

from models import Boundary


def build_matrix_geopandas(lat_min, lat_max, long_min, long_max, cell_size) -> gpd.GeoDataFrame:
    """
    :param lat_min: Minimum latitude value of the bounding box.
    :param lat_max: Maximum latitude value of the bounding box.
    :param long_min: Minimum longitude value of the bounding box.
    :param long_max: Maximum longitude value of the bounding box.
    :param cell_size: Size of each cell in the grid.
    :return: GeoDataFrame containing polygons representing the grid cells in the specified bounding box.

    This method creates a grid of polygons using the given bounding box coordinates and cell size. The grid is created by dividing the bounding box into cells of equal size. The method returns
    * a GeoDataFrame containing the polygons representing the grid cells.

    Example usage:

    lat_min = 40.0
    lat_max = 41.0
    long_min = -74.0
    long_max = -73.0
    cell_size = 0.1

    grid = build_matrix_geopandas(lat_min, lat_max, long_min, long_max, cell_size)
    """
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


def build_matrix(lat_min, lat_max, long_min, long_max, cell_size) -> list[list[Boundary]]:
    """
    Builds a matrix of cells representing chunks of coordinates based on the given parameters.

    :param lat_min: The minimum latitude value.
    :param lat_max: The maximum latitude value.
    :param long_min: The minimum longitude value.
    :param long_max: The maximum longitude value.
    :param cell_size: The size of each cell in the matrix.
    :return: A 2D matrix of cells.

    """
    # Create the latitude and longitude ranges
    lat_range = np.arange(lat_min, lat_max, cell_size)
    long_range = np.arange(long_min, long_max, cell_size)

    # Initialize the 2D matrix
    matrix = np.empty((len(lat_range), len(long_range)), dtype=object)

    # Populate the 2D matrix with cells representing chunks of coordinates
    for i, lat in enumerate(lat_range):
        for j, long in enumerate(long_range):
            cell = Boundary(
                lat_min=lat,
                lat_max=lat + cell_size,
                long_min=long,
                long_max=long + cell_size
            )
            matrix[i, j] = cell

    return matrix


def get_matrix(lat_min: float, lat_max: float, long_min: float, long_max: float, cell_size: float, directory: Path):
    filepath = directory / '1_matrix_file.pickle'

    # check if matrix file exist:
    if filepath.exists():
        with open(filepath, 'rb') as file:
            matrix = pickle.load(file)
    else:
        matrix = build_matrix(lat_min, lat_max, long_min, long_max, cell_size)
        # save the matrix to a file
        with open(filepath, 'wb') as file:
            pickle.dump(matrix, file)

    return matrix
