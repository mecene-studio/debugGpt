import requests
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper

from dotenv import load_dotenv
import os

load_dotenv()


def searchGoggleCustom(query: str):
    items = _searchGoggleCustom(query)
    answer = []

    for i, item in enumerate(items):
        print(i, item["title"])
        print("########################")
        print(item)
        print("########################")
        print()

        answer.append(item["snippet"])
        # answer.append(item["link"])

    return answer


def getLinksFromGoogle(query: str):
    items = _searchGoggleCustom(query)
    links = []

    for i, item in enumerate(items):
        # print(i, item["title"])
        # print("########################")
        # print(item)
        # print("########################")
        # print()

        links.append(item["link"])

    return links


def _searchGoggleCustom(query: str):
    API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY") or "MISSING API KEY"
    GOOGLE_CX = os.getenv("GOOGLE_CX") or "MISSING CX"

    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": API_KEY, "cx": GOOGLE_CX, "q": query, "num": 1}

    res = requests.get(url, params=params)
    # print("res", res)
    data = res.json()
    # print("data", data)
    items = data.get("items", [])

    return items
