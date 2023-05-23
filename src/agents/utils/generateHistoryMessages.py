def generateHistoryMessagesLimited(startingMessages, historyMessages):
    messages = []
    # load the last 5 message pairs from the history
    # get them in historical order

    maxChar = 16_000  # approx 16k tokens is the max for gpt-3.5-turbo
    currentTokenCount = 0
    insertIndex = 0

    for i in range(len(startingMessages)):
        currentTokenCount += len(startingMessages[i]["content"])
        if currentTokenCount > maxChar:
            break
        messages.append(startingMessages[i])
        insertIndex += 1

    addedMessages = 0

    for i in range(len(historyMessages) - 1, 0, -2):
        print("i", i)

        userMessage = historyMessages[i]
        # print("userMessage", userMessage)
        assistantMessage = historyMessages[i - 1]
        # print("assistantMessage", assistantMessage)
        currentTokenCount += len(assistantMessage["content"])
        currentTokenCount += len(userMessage["content"])
        if currentTokenCount > maxChar:
            break
        messages.insert(insertIndex, userMessage)
        messages.insert(insertIndex, assistantMessage)
        addedMessages += 2

    if addedMessages == 0:
        raise Exception(
            "INTERNAL ERROR: no messages were added to the history, new messages are too long"
        )

    return messages


def generateHistoryMessageFull(startingMessages, historyMessages):
    # append the history messages to the starting messages
    messages = startingMessages + historyMessages
    return messages
