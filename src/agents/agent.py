import re
from agents.utils.debuggptprompt import (
    getDebugGptFileMessage,
    getDebugGptPromptMessages,
    getFeedbackFromCodeExecutionPrompt,
    getFeedbackFromUserPrompt,
)
from agents.utils.juniordevprompt import (
    getJuniorDevFileMessage,
    getJuniorDevPromptMessages,
)
from agents.utils.seniordevprompt import (
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
from tools.readFile import readCodeFile, readFileFromTestApp
from tools.runShell import getErrorsFromFile, runShell
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

    def addPlan(self, systemMessages, plan):
        return NotImplementedError

    def startLoop(self, prompt: str):
        # answer = "runCommand(npm run build)"  # hardcode the first command
        # print("initial prompt:\n", prompt)

        userContent = prompt
        plan = ""

        printUser("################## user message : \n" + userContent)

        maxIterations = 100
        autoRunIterations = 0
        for i in range(maxIterations):
            userMessage = {"role": "user", "content": userContent}

            # type: ignore
            # printUser("################## answer from user message : \n" + userContent)

            self.messageHistory.append(userMessage)

            systemMessages = self.addSystemMessage([])

            systemMessages = self.addPlan(systemMessages, plan)

            # limit history to the last 4 messages
            self.messageHistory = self.messageHistory[-4:]

            messages = generateHistoryMessagesTikToken(
                self.promptHistory, self.messageHistory, systemMessages
            )

            # setConsoleColor("yellow")
            # print("\n\n################## messages: \n")
            # for i, message in enumerate(messages):
            #     print(message.get("role"), ":   \n\n")
            #     lines = message.get("content").split("\n")
            #     for line in lines:
            #         print("\t", line)
            #     print("\n")
            # # print("\n################## prompt from user: \n")
            # # print(userContent)
            # resetConsoleColor()

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
            functionName = "NO FUNCTION NAME FOUND"
            arguments = ["DEFAULT ARGUMENTS"]

            try:
                functionName, arguments, plan = parseToolUserAnswer(answer)

                if functionName == "finishedanswer":
                    return f"AGENT FINISHED with message: + \n {arguments[0]}"
                print("WILL RUN COMMAND:", functionName)
                for i, arg in enumerate(arguments):
                    print("ARGUMENT", i, ": ", arg)
            except Exception as e:
                print(e)
                userContent = "INTERNAL ERROR: " + str(e)

            if autoRunIterations <= 0:
                # wait for user input to continue
                inputted = input(
                    "\nPress Enter to run, Type 'run -N' to run it for N iterations, Type 't' to tell agent to try again or type anything to send it as feedback:"
                )

                # check for run command
                if re.match(r"run\s*-\s*\d*", inputted):
                    autoRunIterations = int(inputted.split("-")[1])
                    print("auto running for", autoRunIterations, "iterations...")

                if inputted == "" or autoRunIterations > 0:
                    print("Running the command...")
                    output = executeToolOrAgent(functionName, arguments)

                    setConsoleColor("yellow")
                    print("\n################## output from tool: \n")
                    print(output)
                    resetConsoleColor()

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

            else:
                autoRunIterations -= 1
                print("Auto Running the command...")
                output = executeToolOrAgent(functionName, arguments)
                userContent = getFeedbackFromCodeExecutionPrompt(
                    functionName, output  # type: ignore
                )

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


class DebugGpt(Agent):
    def __init__(self):
        super().__init__()
        self.name = "DebugGpt"

    def getPromptMessages(self):
        return getDebugGptPromptMessages()

    def addSystemMessage(self, systemMessages):
        fileSystemMessage = getDebugGptFileMessage()

        systemMessages.append(fileSystemMessage)

        return systemMessages

    def speak(self, state):
        if state:
            setConsoleColor("cyan")
        else:
            resetConsoleColor()

    def addPlan(self, systemMessages, plan):
        return systemMessages


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
    if functionName == "NO FUNCTION NAME FOUND":
        return "NO FUNCTION NAME FOUND"
    if functionName == "juniorDevGpt":
        agent = JuniorDev()
        return agent.startLoop(arguments[0])
    elif functionName == "searchGpt":
        return searchGoggleCustom(arguments[0])
    elif functionName == "getBugs":
        return getErrorsFromFile("", allFiles=True)
    elif functionName == "runShell":
        return runShell(arguments[0])
    elif functionName == "openFile":
        return readFileFromTestApp(arguments[0])
    elif functionName == "editFile":
        initialPrompt = "You are editing the file below:"

        fileContent = readFileFromTestApp(arguments[0])
        return (
            fileContent
            + "\n\nUse the writeFile tool to overwrite the file with your changes"
        )
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
        return f"INTERNAL ERROR: command `{functionName}` not found"


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
        explanation, commands = answer.split("¬", 1)
        commands = commands.split("¬")[0]

        plan = explanation
        firstCommand = commands

        # index, answer = answer.split(":::", 1)
        # firstCommand = answer.split(":::", 1)[0].strip()

        # # if firstCommand ends with \n2, \n1 or any number, remove it
        # if firstCommand[-1].isdigit():
        #     firstCommand = firstCommand.rsplit("\n", 1)[0]

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
