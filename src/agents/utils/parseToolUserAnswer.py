from agents.debugGpt.debugGptPrompt import getFeedbackFromCodeExecutionPrompt
from tools.executeTool import executeTool


def parseAndExecuteTool(answer):
    try:
        functionName, arguments = parseToolUserAnswer(answer)

        print("shell output:\n ")
        output = executeTool(functionName, arguments)

        return getFeedbackFromCodeExecutionPrompt(functionName, output)

    except Exception as e:
        print(e)
        return "INTERNAL ERROR: " + str(e)


def parseToolUserAnswer(answer):
    # writeFile(components/LandingPage.tsx, ```import React from "react";
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
        functionName, arguments = answer.split("(", 1)
        arguments = arguments[:-1]
        arguments = arguments.split(",", 1)

        for i in range(len(arguments)):
            arguments[i] = arguments[i].strip()

        return functionName, arguments
    except:
        raise Exception("Invalid answer format")
