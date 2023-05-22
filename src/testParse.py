from agents.agent import parseToolUserAnswer
from agents.utils.generateHistoryMessages import (
    generateHistoryMessages,
    generateHistoryMessagesComplicated,
)


def testHistory():
    startingMessages = [{"role": "system", "content": "your are a gpt"}]
    historyMessages = [
        {
            "role": "user",
            "content": "user0user0user0user0user0user0user0user0user0user0user0user0user0user0user0user0user0user0user0user0user0",
        },
        {
            "role": "system",
            "content": "system1system1system1system1system1system1system1system1system1system1system1system1system1system1system1system1",
        },
        {
            "role": "user",
            "content": "user2user2user2user2user2user2user2user2user2user2user2user2user2user2user2user2user2user2user2user2user2user2user2",
        },
        {
            "role": "system",
            "content": "system3system3system3system3system3system3system3system3system3system3system3system3system3system3system3system3",
        },
        {
            "role": "user",
            "content": "user4user4user4user4user4user4user4user4user4user4user4user4user4user4user4user4user4user4user4user4user4user4user4user4",
        },
        {
            "role": "system",
            "content": "system5system5system5system5system5system5system5system5system5system5system5system5system5system5system5system5",
        },
    ]
    messages = generateHistoryMessagesComplicated(startingMessages, historyMessages)
    print("\n\nmessages:", messages, "\n\n")
    for message in messages:
        print(message.get("role"), ":\n", message.get("content"))


def testParseTools():
    answer = """1 ::: runCommand(npm run lint) - To check for any linting errors in the code.
2 ::: runCommand(npm run build) - To build the application.
3 ::: runCommand(npm start) - To start the application and check if it is running correctly.
4 ::: If there are any errors, use the readFile tool to read the error message and fix the error accordingly.
5 ::: Once the application is running correctly, use the finishedanswer tool to let the user know that the application has been built successfully."""

    functionName, arguments = parseToolUserAnswer(answer)
    print("functionName:", functionName)
    print("arguments:", arguments)


if __name__ == "__main__":
    testParseTools()
