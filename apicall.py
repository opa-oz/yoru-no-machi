import asyncio
from pathlib import Path

import aiohttp
from aiohttp import ClientSession


async def fetch_url(session: ClientSession, url: str, output_directory: Path, index: int) -> str:
    """
    Fetches content from the given URL using the provided session and saves it to a file in the output_directory.

    :param session: An instance of `ClientSession` for making HTTP requests.
    :param url: The URL from which to fetch the content.
    :param output_directory: The directory in which to save the fetched content.
    :param index: The index used to generate the filename for saving the content.
    :return: The path of the saved file as a string.
    """
    async with session.get(url) as response:
        content = await response.text()
        target = output_directory / 'chunk_{:04d}.osm'.format(index)

        with open(target, 'w') as f:
            f.write(content)

        print(f"Done #{index}")
        return str(target)


async def batch_process(urls: list[str], output_directory: Path) -> list[Path]:
    """
    Process a batch of URLs asynchronously and save the downloaded files to the specified output directory.

    :param urls: A list of URLs to be processed.
    :type urls: list[str]
    :param output_directory: The directory where the downloaded files will be saved.
    :type output_directory: Path
    :return: A list of Path objects representing the paths to the saved files.
    :rtype: list[Path]
    """
    conn = aiohttp.TCPConnector(limit=5)  # limit concurrency to 5

    async with ClientSession(connector=conn) as session:
        tasks = []
        for i in range(len(urls)):
            tasks.append(fetch_url(session, urls[i], output_directory, i))

        return list(map(Path, await asyncio.gather(*tasks)))
