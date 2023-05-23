from agents.agent import parseToolUserAnswer
from agents.utils.generateHistoryMessages import (
    generateHistoryMessageFull,
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
    messages = generateHistoryMessagesComplicated(
        startingMessages, historyMessages)
    print("\n\nmessages:", messages, "\n\n")
    for message in messages:
        print(message.get("role"), ":\n", message.get("content"))


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
    testParseTools()
