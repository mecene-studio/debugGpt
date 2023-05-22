from agents.agentPrompt import getFeedbackFromCodeExecutionPrompt
from agents.utils.juniordevprompt import getJuniorDevPromptMessages
from agents.utils.seniordevprompt import (
    getFeedbackFromUserPrompt,
    getSeniorDevPromptMessages,
)
from agents.utils.generateHistoryMessages import generateHistoryMessages
from cleanConsole import printUser, resetConsoleColor, setConsoleColor
from openaiLib.chatGpt import askChatGpt
from tools.listFiles import listFilesFromTestApp
from tools.moveFile import moveFileFromTestApp
from tools.readFile import readFileFromTestApp
from tools.runShell import runShell
from tools.searchGoogle import searchGoggleCustom
from tools.stackOverflow import searchStackOverflow
from tools.writeFile import writeFileToTestApp


class Agent:
    def __init__(self):
        self.messageHistory = []
        self.promptHistory = self.getPromptMessages()
        self.name = "DefaultAgent"

    def getPromptMessages(self):
        raise NotImplementedError

    def speak(self, state):
        raise NotImplementedError

    def startLoop(self, prompt):
        # answer = "runCommand(npm run build)"  # hardcode the first command
        # print("first command:\n", answer)

        userContent = prompt

        maxIterations = 50
        for i in range(maxIterations):
            userMessage = {"role": "user", "content": userContent}

            # type: ignore
            printUser("userMessage: \n" + userMessage.get("content"))

            self.messageHistory.append(userMessage)

            messages = generateHistoryMessages(
                self.promptHistory, self.messageHistory)

            # print("\n\n################## messages: \n")
            # for i, message in enumerate(messages):
            #     print(message.get("role"), ":", message.get("content"))

            self.speak(True)
            print("\n\n################## answer from", self.name, ": \n")
            answer = askChatGpt(messages)
            self.speak(False)

            assistantMessage = {
                "role": "assistant",
                "content": answer,
            }

            self.messageHistory.append(assistantMessage)

            userContent = "DEFAULT USER CONTENT"

            # wait for user input to continue
            inputted = input(
                "\nPress Enter to continue, Type 't' to tell agent to try again or type anything to send it as feedback:"
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

        return f"INTERNAL ERROR: agent {self.name} reached maxIterations: {maxIterations} without reaching endDebugging"


class JuniorDev(Agent):
    def __init__(self):
        super().__init__()
        self.name = "JuniorDev"

    def getPromptMessages(self):
        return getJuniorDevPromptMessages()

    def speak(self, state):
        if state:
            setConsoleColor("blue")
        else:
            resetConsoleColor()


class SeniorDev(Agent):
    def __init__(self):
        super().__init__()
        self.name = "SeniorDev"

    def getPromptMessages(self):
        return getSeniorDevPromptMessages()

    def speak(self, state):
        if state:
            setConsoleColor("magenta")
        else:
            resetConsoleColor()


def executeToolOrAgent(functionName, arguments):
    if functionName == "juniorDevGpt":
        agent = JuniorDev()
        return agent.startLoop(arguments[0])
    elif functionName == "runCommand":
        return runShell(arguments[0])
    elif functionName == "readFile":
        return readFileFromTestApp(arguments[0])
    elif functionName == "listFiles":
        return listFilesFromTestApp()
    elif functionName == "moveFile":
        return moveFileFromTestApp(arguments[0], arguments[1])
    elif functionName == "searchStackOverflow":
        return searchStackOverflow(arguments[0])
    elif functionName == "searchGoogle":
        return searchGoggleCustom(arguments[0])
    elif functionName == "writeFile":
        return writeFileToTestApp(arguments[0], arguments[1].replace("```", ""))
    elif functionName == "endDebugging":
        return "Debugging ended"
    else:
        return "INTERNAL ERROR: functionName not recognized"


def parseAndExecuteTool(answer):
    try:
        functionName, arguments = parseToolUserAnswer(answer)

        print("shell output:\n ")
        output = executeToolOrAgent(functionName, arguments)

        return getFeedbackFromCodeExecutionPrompt(functionName, output)

    except Exception as e:
        print(e)
        return "INTERNAL ERROR: " + str(e)


def parseToolUserAnswer(answer):
    # 1 ::: writeFile(components/LandingPage.tsx, ```import React from "react";
    # import s from "./LandingPage.module.scss";

    # const LandingPage = () => {
    # return (
    #     <div className={s.container}>
    #         <span>hello</span>
    #     </div>
    # );
    # };

    # export default LandingPage;
    # ```)

    try:
        index, answer = answer.split(":::", 1)
        print("index:", index)
        print("\n\nanswer:", answer, "\n\n")
        functionName, arguments = answer.split("(", 1)
        arguments = arguments.split(") -", 1)[0]
        arguments = arguments.split(",", 1)

        for i in range(len(arguments)):
            arguments[i] = arguments[i].strip()

        return functionName, arguments
    except:
        raise Exception("Invalid answer format")
