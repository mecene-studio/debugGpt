from agents.agent import parseToolUserAnswer
from agents.utils.generateHistoryMessages import (
    generateHistoryMessagesTikToken,
)
from agents.utils.juniordevprompt import getJuniorDevPromptMessages


def testHistory():
    startingMessages = [{"role": "system", "content": "your are a gpt"}]
    historyMessages = [
        {
            "role": "user",
            "content": "use0",
        },
        {
            "role": "assistant",
            "content": "assistant1",
        },
        {
            "role": "user",
            "content": "user2",
        },
        {
            "role": "assistant",
            "content": "assistant3",
        },
        {
            "role": "user",
            "content": "user4",
        },
    ]
    messages = generateHistoryMessagesTikToken(startingMessages, historyMessages)
    print("\n\nmessages:", messages, "\n\n")
    for message in messages:
        print(message.get("role"), ":\n", message.get("content")[0:100])


def testParseTools():
    answer = """
    
    1 ::: listFiles() - To see what files are available to build the application.
2 ::: juniorDevGpt(build the application) - To build the application and fix any errors.
3 ::: juniorDevGpt(re-build the application) - To make sure there are no errors.
    
    """

    functionName, arguments = parseToolUserAnswer(answer)
    print("functionName:", functionName)
    # print("arguments:", arguments)
    for i, arg in enumerate(arguments):
        print("argument", i, ":", arg)


if __name__ == "__main__":
    testHistory()
