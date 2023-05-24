from agents.agent import parseToolUserAnswer
from agents.utils.generateHistoryMessages import (
    generateHistoryMessagesTikToken,
)
from agents.utils.juniordevprompt import getJuniorDevPromptMessages


def testHistory():
    startingMessages = [
        {"role": "system", "content": "your are a gpt"},
        {
            "role": "system",
            "content": "be helpful",
        },
    ]
    historyMessages = [
        {
            "role": "user",
            "content": "user0",
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

    systemMessages = [
        {
            "role": "system",
            "content": "system0",
        },
        {
            "role": "system",
            "content": "system1",
        },
    ]

    messages = generateHistoryMessagesTikToken(
        startingMessages, historyMessages, systemMessages
    )
    print("\n\nmessages:", messages, "\n\n")
    for message in messages:
        print(message.get("role"), ":", message.get("content")[0:100])


def testParseTools():
    answer = """
    Yes, i can do that
    
    1 ::: runCommand (npm run build)

2 ::: listFiles()

3 ::: readFile(app/page.tsx)

4 ::: readFile(components/LandingPage/LandingPage.tsx)

5 ::: readFile(components/LandingPage/LandingPage.module.scss)

6 ::: readFile(components/LandingPage/test.tsx)

7 ::: readFile(components/AppLayout.tsx)

8 ::: readFile(components/Button.tsx)

9 ::: readFile(components/Footer.tsx)

10 ::: readFile(components/Header.tsx)

11 ::: readFile(components/Logo.tsx)

12 ::: runCommand(npm run lint) [Note: This command is not allowed, so I will skip it]

13 ::: finishedanswer (I have built the application and checked all the files for errors.)

If you want me to do something else, just ask me.
"""

    functionName, arguments, plan = parseToolUserAnswer(answer)
    print("functionName:", functionName)
    # print("arguments:", arguments)
    for i, arg in enumerate(arguments):
        print("argument", i, ":", arg)


if __name__ == "__main__":
    testHistory()
