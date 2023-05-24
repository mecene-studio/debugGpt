import re
from agents.agentPrompt import getFeedbackFromCodeExecutionPrompt, getPlanMessage
from agents.utils.juniordevprompt import (
    getJuniorDevFileMessage,
    getJuniorDevPromptMessages,
)
from agents.utils.seniordevprompt import (
    getFeedbackFromUserPrompt,
    getSeniorDevPromptMessages,
)
from agents.utils.generateHistoryMessages import (
    generateHistoryMessageFull,
    generateHistoryMessagesLimited,
    generateHistoryMessagesTikToken,
)
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

    def addSystemMessage(self, systemMessages):
        return systemMessages

    def startLoop(self, prompt: str):
        # answer = "runCommand(npm run build)"  # hardcode the first command
        # print("initial prompt:\n", prompt)

        userContent = prompt
        plan = ""

        maxIterations = 50
        for i in range(maxIterations):
            # TODO: switch role to user
            userMessage = {"role": "user", "content": userContent}

            # type: ignore
            printUser("userMessage: \n" + userContent)

            self.messageHistory.append(userMessage)

            systemMessages = self.addSystemMessage([])

            planMessage = getPlanMessage(plan)
            if planMessage:
                systemMessages.append(planMessage)

            messages = generateHistoryMessagesTikToken(
                self.promptHistory, self.messageHistory, systemMessages
            )

            setConsoleColor("yellow")
            print("\n\n################## messages: \n")
            for i, message in enumerate(messages):
                print(message.get("role"), ":   \n\n")
                lines = message.get("content").split("\n")
                for line in lines:
                    print("\t", line)
                print("\n")
            resetConsoleColor()

            self.speak(True)
            print("\n\n################## answer from", self.name, ": \n")
            answer = askChatGpt(messages)
            print("\n################## ")
            self.speak(False)

            assistantMessage = {
                "role": "assistant",
                "content": answer,
            }

            self.messageHistory.append(assistantMessage)

            userContent = "DEFAULT USER CONTENT"
            functionName = "DEFAULT FUNCTION NAME"
            arguments = ["DEFAULT ARGUMENTS"]

            try:
                functionName, arguments, plan = parseToolUserAnswer(answer)

                if functionName == "finishedanswer":
                    return f"AGENT FINISHED with message: + \n {arguments[0]}"
                print("WILL RUN:", functionName)
                for i, arg in enumerate(arguments):
                    print("ARG", i, ": ", arg)
            except Exception as e:
                print(e)
                userContent = "INTERNAL ERROR: " + str(e)

            # wait for user input to continue
            inputted = input(
                "\nPress Enter to run, Type 't' to tell agent to try again or type anything to send it as feedback:"
            )
            if inputted == "":
                print("Running the command...")
                output = executeToolOrAgent(functionName, arguments)
                userContent = getFeedbackFromCodeExecutionPrompt(
                    functionName, output  # type: ignore
                )

            elif inputted == "t" or inputted == "T":
                print("Trying again...")
                userContent = getFeedbackFromUserPrompt("Try again")
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

    def addSystemMessage(self, systemMessages):
        fileSystemMessage = getJuniorDevFileMessage()

        systemMessages.append(fileSystemMessage)

        return systemMessages

    def speak(self, state):
        if state:
            setConsoleColor("cyan")
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
    elif functionName == "searchGpt":
        return searchGoggleCustom(arguments[0])
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
        # explanation, commands = answer.split("$$$", 1)
        # commands = commands.split("$$$")[0]

        plan = answer

        index, answer = answer.split(":::", 1)
        firstCommand = answer.split(":::", 1)[0].strip()

        # if firstCommand ends with \n2, \n1 or any number, remove it
        if firstCommand[-1].isdigit():
            firstCommand = firstCommand.rsplit("\n", 1)[0]

        functionName, arguments = firstCommand.split("(", 1)
        arguments_reversed = arguments[::-1]
        arguments_reversed = arguments_reversed.split(")", 1)[1]
        arguments = arguments_reversed[::-1]

        argumentsList = splitByCommaButNotByCodeblock(arguments)
        # split by , but not by , inside ``` ```

        functionName = functionName.strip()

        for i in range(len(argumentsList)):
            argumentsList[i] = argumentsList[i].strip()

        return functionName, argumentsList, plan
    except:
        raise Exception("Invalid answer format")


def splitByCommaButNotByCodeblock(string):
    code_blocks = re.findall(r"```[\s\S]+?```", string)  # Extract code blocks
    placeholders = []  # Placeholder strings for code blocks
    for i, block in enumerate(code_blocks):
        placeholder = f"__CODEBLOCK_{i}__"
        string = string.replace(block, placeholder)
        placeholders.append(placeholder)

    parts = re.split(
        r",(?![^`]*`[^`]*`)", string
    )  # Split by comma excluding code blocks

    # Replace back the code blocks
    for i, placeholder in enumerate(placeholders):
        parts = [part.replace(placeholder, code_blocks[i]) for part in parts]

    return parts
