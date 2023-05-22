import requests
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper

from dotenv import load_dotenv
import os

load_dotenv()


def searchGoggleCustom(query: str):
    queryClean = query.replace("```", "").replace('"', "").replace("'", "")
    print("queryClean:", queryClean)
    items = _searchGoggleCustom(queryClean)
    answer = []

    for i, item in enumerate(items):
        # print(i, item["title"])
        # print("########################")
        # print(item)
        # print("########################")
        # print()
        outputItem = {
            "title": item["title"],
            "snippet": item["snippet"],
            "link": item["link"],
        }
        answer.append(outputItem)
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
    GOOGLE_CX_ID = os.getenv("GOOGLE_CX_ID") or "MISSING CX"

    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": API_KEY, "cx": GOOGLE_CX_ID, "q": query, "num": 3}

    res = requests.get(url, params=params)
    # print("res", res)
    data = res.json()
    if "error" in data:
        raise Exception(data["error"]["message"])
    items = data.get("items", [])

    return items
