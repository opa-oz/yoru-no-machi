import asyncio
import datetime
from pathlib import Path

from apicall import batch_process
from config import get_config
from geoframe import get_geoframe
from matrix import get_matrix
import matplotlib.pyplot as plt
import osmnx as ox
import networkx as nx

from utils import build_api_url

base_dir = Path(__file__).resolve().parent


async def main():
    print(f"{datetime.datetime.now()}: Starting program...")
    config = get_config(base_dir)

    output_dir = base_dir / 'output' / config.name
    output_dir.mkdir(exist_ok=True, parents=True)

    gfeatures = ox.features_from_place('Озинки', tags={'building': True})
    ox.plot_footprints(
        gfeatures,
        show=False,
        save=True,
        filepath=str(base_dir / "1_result.png"),
    )

    groutes = ox.graph_from_place('Озинки', network_type='drive')
    ox.plot_graph(
        groutes,
        filepath=str(base_dir / "0_result.png"),
        show=False,
        save=True,
        node_size=0
    )



async def mainold():
    print(f"{datetime.datetime.now()}: Starting program...")
    config = get_config(base_dir)

    output_dir = base_dir / 'output' / config.name
    output_dir.mkdir(exist_ok=True, parents=True)
    urls = []
    matrix = get_matrix(
        config.boundaries.lat_min,
        config.boundaries.lat_max,
        config.boundaries.long_min,
        config.boundaries.long_max,
        config.cell_size,
        directory=output_dir)

    print(f"{datetime.datetime.now()}: Matrix created.")

    for row in matrix:
        for cell in row:
            url = build_api_url(cell.long_min, cell.lat_min, cell.long_max, cell.lat_max)
            urls.append(url)

    print(f"{datetime.datetime.now()}: URL collection completed... Awaiting batch processing...")

    paths = await batch_process(urls, output_dir)

    print(f"{datetime.datetime.now()}: Batch processing completed... Starting aggregation of data...")

    all_gdf = get_geoframe(paths, output_dir)

    # Plot the GeoDataFrame
    all_gdf.plot()

    # Save the figure
    plt.savefig(output_dir / "0_result.png")

    print(f"{datetime.datetime.now()}: Aggregation and plot creation completed... Program ended.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
