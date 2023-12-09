import os


def clear_console():
    """
    Clears the console screen.

    :return: None
    """
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
