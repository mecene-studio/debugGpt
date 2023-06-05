import openai
from dotenv import load_dotenv
import os
import time

import requests

from agents.utils.generateHistoryMessages import (
    getTotalTokensForMessages,
    printStatsForPastRequests,
)


model = "gpt-3.5-turbo"  # "gpt-4", gpt-4-0314, gpt-4-32k, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-0301

pastRequests = []
nbBackoffRetries = 0


def askChatGpt(promptMessages, max_tokens=1024):
    load_dotenv()

    tokensForThisRequest = getTotalTokensForMessages(promptMessages)
    request = {
        "date": time.time(),
        "tokens": tokensForThisRequest,
    }
    pastRequests.append(request)

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "MISSING API KEY"
    openai.api_key = OPENAI_API_KEY

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=promptMessages,
            temperature=0,
            max_tokens=max_tokens,
            stream=True,  # this time, we set stream=True
        )

        answer = ""

        deltas = []

        for chunk in response:
            delta = chunk["choices"][0]["delta"]  # type: ignore

            if delta.get("content"):
                text = delta["content"]
                answer += text
                print(text, end="")
            deltas.append(delta)

        print("\n")

        return answer

    except Exception as e:
        print("ERROR asking chatgpt:", e)
        print("tokensForThisRequest:", tokensForThisRequest)
        printStatsForPastRequests(pastRequests)
        # wait 60 seconds and try again
        global nbBackoffRetries
        nbBackoffRetries += 1
        timeOff = 60 * nbBackoffRetries
        print("waiting", timeOff, "seconds and trying again")
        time.sleep(timeOff)
        return askChatGpt(promptMessages, max_tokens)


def getAvailibleModels():
    url = "https://api.openai.com/v1/models"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("OPENAI_API_KEY"),  # type: ignore
    }

    res = requests.get(url, headers=headers)
    print("res:", res)
    print("res.json():", res.json())
