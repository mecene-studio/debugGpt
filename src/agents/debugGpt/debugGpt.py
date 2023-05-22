from agents.debugGpt.debugGptPrompt import (
    getDebugGptPromptMessages,
    getFeedbackFromCodeExecutionPromptMessage,
)
from agents.utils.generateHistoryMessages import generateHistoryMessages
from agents.utils.parseToolUserAnswer import parseToolUserAnswer
from tools.executeTool import executeTool

from openaiLib.chatGpt import askChatGpt


def startDebugGpt():
    startingMessages = getDebugGptPromptMessages()
    historyMessages = []

    answer = "runCommand(npm run build)"  # hardcode the first command

    maxIterations = 50
    for i in range(maxIterations):
        assistantMessage = {
            "role": "assistant",
            "content": answer,
        }

        historyMessages.append(assistantMessage)

        functionName, arguments = parseToolUserAnswer(answer)

        if functionName == "endDebugging":
            return "Debugging ended"

        print("shell output:\n ")
        output = executeTool(functionName, arguments)

        userMessage = getFeedbackFromCodeExecutionPromptMessage(functionName, output)

        print("userMessage: \n", userMessage.get("content"))

        historyMessages.append(userMessage)

        messages = generateHistoryMessages(startingMessages, historyMessages)

        # print("\n\n################## messages: \n")
        # for i, message in enumerate(messages):
        #     print(message.get("role"), ":", message.get("content"))

        print("\n\n################## answer from askDebugGpt: \n")
        answer = askChatGpt(messages)

        # wait for user input to continue
        input("\nPress Enter to continue...")

    return f"INTERNAL ERROR: askDebugGpt reached maxIterations: {maxIterations} without reaching endDebugging"
