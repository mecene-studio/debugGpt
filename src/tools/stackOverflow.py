from stackapi import StackAPI

from tools.searchGoogle import getLinksFromGoogle


def searchStackOverflow(query):
    query = query.replace('"', "").replace("'", "")
    newQuery = f"site:stackoverflow.com {query}"
    print("stack overflow query")
    print(newQuery, "\n")
    links = getLinksFromGoogle(newQuery)

    if len(links) == 0:
        return "STACKOVERFLOW: No results found, try a different query."

    # print("links", links)
    link = links[0]

    # https://stackoverflow.com/questions/71433951/module-not-found-cant-resolve-next-js-typescript
    postId = link.split("https://stackoverflow.com/questions/")[1].split("/")[0]

    # print("postId", postId)

    return getAnswersForStackOverflowPost(postId)


def getAnswersForStackOverflowPost(postId):
    SITE = StackAPI("stackoverflow")

    # res = SITE.fetch("questions/{ids}", ids=[44439205], filter="withbody")
    # # print("res", res)
    # items = res["items"]
    # item = items[0]

    # print("title:", item["title"])

    # body = item["body"]
    # print("body:\n", body)

    # # for item in items:
    # #     print("item\n", item)

    res = SITE.fetch(
        "questions/{ids}/answers",
        ids=[postId],
        filter="withbody",
        # max=1,
        sort="votes",
    )

    # print("res", res)
    items = res["items"]
    # print("items", items)
    item = items[0]

    # for item in items:
    #     print("item\nn", item, "\n\n")

    body = item["body"]
    # print("body:\n", body)

    return body
