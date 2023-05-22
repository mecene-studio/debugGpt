def generateHistoryMessagesComplicated(startingMessages, historyMessages):
    messages = []
    # load the last 5 message pairs from the history
    # get them in historical order
    # maxHistoryMessagesPairs = 5
    maxChar = 16_000  # approx 16k tokens is the max for gpt-3.5-turbo
    currentTokenCount = 0
    insertIndex = 0

    for i in range(len(startingMessages)):
        currentTokenCount += len(startingMessages[i]["content"])
        if currentTokenCount > maxChar:
            break
        messages.append(startingMessages[i])
        insertIndex += 1

    maxHistoryMessagesPairs = 10
    for i in range(0, maxHistoryMessagesPairs, 2):
        print("i", i)

        userMessage = historyMessages[i]
        assistantMessage = historyMessages[i + 1]
        currentTokenCount += len(assistantMessage["content"])
        currentTokenCount += len(userMessage["content"])
        if currentTokenCount > maxChar:
            break
        messages.insert(insertIndex, userMessage)
        messages.insert(insertIndex, assistantMessage)

    return messages


def generateHistoryMessages(startingMessages, historyMessages):
    # append the history messages to the starting messages
    messages = startingMessages + historyMessages
    return messages
