import datetime
from pathlib import Path

import geopandas as gpd
import osmnx as ox
from osmnx._errors import InsufficientResponseError


def get_geoframe(paths: list[Path], output_dir: Path) -> gpd.GeoDataFrame:
    all_gdf = gpd.GeoDataFrame()

    gdf_file = output_dir / "geodataframe.geojson"

    # If GeoDataFrame file exists, loads it from the file, otherwise processes the paths
    if gdf_file.exists():
        print(f"{datetime.datetime.now()}: Loading GeoDataFrame from file...")
        all_gdf = gpd.read_file(gdf_file)
    else:
        for i, chunkfile in enumerate(paths):
            print(f"{datetime.datetime.now()}: Processing chunk file {i + 1} of {len(paths)}...")

            if i > 5:
                break

            try:
                # Load the OSM data from the .osm file
                G = ox.graph_from_xml(chunkfile)

                # Convert the OSM data to a GeoDataFrame
                gdf = ox.graph_to_gdfs(G)

                # Append the GeoDataFrame to the complete set
                all_gdf = all_gdf.sjoin(gdf)
            except InsufficientResponseError as e:
                print(f"{datetime.datetime.now()}: 🟡 Chunk file {i + 1} is empty /", e)
            except ValueError as e:
                print(f"{datetime.datetime.now()}: 🔴 Chunk file `{chunkfile}` /", e)

        # Save GeoDataFrame to file
        print(f"{datetime.datetime.now()}: Saving GeoDataFrame to file...")
        all_gdf.to_file(str(gdf_file), driver='GeoJSON')

    return all_gdf
