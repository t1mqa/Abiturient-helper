import requests


def request_it(link: str) -> requests.Response:
    return requests.get(link)
