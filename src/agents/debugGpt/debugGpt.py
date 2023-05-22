from agents.debugGpt.debugGptPrompt import (
    getDebugGptPromptMessages,
    getFeedbackFromCodeExecutionPrompt,
    getFeedbackFromUserPrompt,
)
from agents.utils.generateHistoryMessages import generateHistoryMessages
from agents.utils.parseToolUserAnswer import parseAndExecuteTool, parseToolUserAnswer
from tools.executeTool import executeTool

from openaiLib.chatGpt import askChatGpt


def startDebugGpt():
    startingMessages = getDebugGptPromptMessages()
    historyMessages = []

    answer = "runCommand(npm run build)"  # hardcode the first command
    print("first command:\n", answer)

    maxIterations = 50
    for i in range(maxIterations):
        assistantMessage = {
            "role": "assistant",
            "content": answer,
        }

        historyMessages.append(assistantMessage)

        userContent = "DEFAULT USER CONTENT"

        # wait for user input to continue
        inputted = input(
            "\nPress Enter to continue, Type 't' to tell debugGpt to try again or type anything to send it as feedback:"
        )
        if inputted == "":
            print("Continuing...")
            userContent = parseAndExecuteTool(answer)
        elif inputted == "t" or inputted == "T":
            print("Trying again...")
            userContent = getFeedbackFromUserPrompt("Try something else")
        else:
            print("sending feedback...")
            print("feedback:", inputted)
            userContent = getFeedbackFromUserPrompt(inputted)

        userMessage = {"role": "user", "content": userContent}

        print("userMessage: \n", userMessage.get("content"))

        historyMessages.append(userMessage)

        messages = generateHistoryMessages(startingMessages, historyMessages)

        # print("\n\n################## messages: \n")
        # for i, message in enumerate(messages):
        #     print(message.get("role"), ":", message.get("content"))

        print("\n\n################## answer from askDebugGpt: \n")
        answer = askChatGpt(messages)

    return f"INTERNAL ERROR: askDebugGpt reached maxIterations: {maxIterations} without reaching endDebugging"
