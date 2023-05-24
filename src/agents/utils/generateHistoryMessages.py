import json
import tiktoken


def generateHistoryMessagesLimited(startingMessages, historyMessages):
    messages = []
    # load the last 5 message pairs from the history
    # get them in historical order

    maxChar = 160_000  # approx 16k tokens is the max for gpt-3.5-turbo
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

    print("current token count:", currentTokenCount)

    if addedMessages == 0:
        raise Exception(
            "INTERNAL ERROR: no messages were added to the history, new messages are too long"
        )

    return messages


def generateHistoryMessagesTikToken(startingMessages, historyMessages, systemMessages):
    # enc = tiktoken.get_encoding("cl100k_base")
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    maxTokens = 4096 - 1024
    currentTokenCount = 0
    insertIndex = 0

    messages = []

    # add starting messages
    for i in range(len(startingMessages)):
        currentTokenCount += len(enc.encode(startingMessages[i]["content"]))
        if currentTokenCount > maxTokens:
            break
        messages.append(startingMessages[i])
        insertIndex += 1

    # add system messages
    for i in range(len(systemMessages)):
        message = systemMessages[i]
        messageTokens = len(enc.encode(message["content"]))
        if currentTokenCount + messageTokens > maxTokens:
            break
        currentTokenCount += messageTokens
        messages.append(message)

    # append last user message
    message = historyMessages[-1]
    messageTokens = len(enc.encode(message["content"]))
    if currentTokenCount + messageTokens > maxTokens:
        raise Exception(
            json.dumps(messages)
            + "INTERNAL ERROR: no messages were added to the history, new messages are too long"
        )
    currentTokenCount += messageTokens
    messages.append(message)

    # add history messages in reverse order until we reach the token limit
    for i in range(len(historyMessages) - 2, -1, -1):
        message = historyMessages[i]
        messageTokens = len(enc.encode(message["content"]))
        if currentTokenCount + messageTokens > maxTokens:
            break
        currentTokenCount += messageTokens
        messages.insert(insertIndex, message)

    print("total token count:", currentTokenCount)

    return messages


def generateHistoryMessageFull(startingMessages, historyMessages):
    # append the history messages to the starting messages
    messages = startingMessages + historyMessages
    return messages
