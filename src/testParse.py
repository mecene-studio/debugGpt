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
    answer = """*** To build the application, we need to make sure there are no errors in the code, and then run the build command ***
$$$
0 ::: juniorDevGpt ( ``` printlen(432,pfds ) ```, yeah for sure ) - this is a test
1 ::: juniorDevGpt ( lint the application and fix any errors ) - wow it sure looks good here
$$$"""

    functionName, arguments = parseToolUserAnswer(answer)
    print("functionName:", functionName)
    # print("arguments:", arguments)
    for i, arg in enumerate(arguments):
        print("argument", i, ":", arg)


if __name__ == "__main__":
    testParseTools()
