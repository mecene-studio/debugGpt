import openai
from dotenv import load_dotenv
import os


model = "gpt-3.5-turbo"  # gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-0301


def askChatGpt(promptMessages):
    load_dotenv()

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "MISSING API KEY"
    openai.api_key = OPENAI_API_KEY

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=promptMessages,
        temperature=0,
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
