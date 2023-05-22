
import agents.utils.basicprompts as p

system_init = """
Your name is juniordevGpt, you are a junior full-stack developper powered by chatGpt. 
Your goal is to answer the command given to you, and send the result to the user.
You are a very good developer, and you know how to write clean, maintainable code.
You also are very good at finding errors in code, and you can fix them easily.
Even the most complex errors, you are able to fix them, by asking yourself the right questions and using all the tools at your disposal.
You don't have to answer the question right away, you can take your time to think about it, and then answer it.

"""

reevaluateAtEachStep = """
Each command will be executed by the agent you chose, and the result will be sent to you.
You will have to analyze the result, and decide what to do next.
You could continue with the original plan, or change the plan based on the result."""

tools_list = """
1: searchDuckDuckGo - to search for information
2: writeFile - to write code in a file
3: readFile - to read code from a file
4: listFiles - to list the files in the workspace to know what files are available to read or write
5: generateCode - to generate code using by giving a prompt to the GPT-3-5-turbo model
6: finishedanswer - to finish your answer and send it to the user
"""

agents_list = """
0: completePlan - end the conversation once the plan is executed
1: searchGpt - give a query and receive a summary of the first results of a google search
2: juniorDevGpt - give a the summary of the code you want to generate, and the code will be generated
"""

testUserPrompt = """Code an app that is tinder for dogs"""

tools = p.tools_init + tools_list
agents = p.agents_init + agents_list


def getSeniorDevGptPromptMessages():
    plannerPrompt = system_init + agents + reevaluateAtEachStep

    promptMessage = {"role": "system", "content": plannerPrompt}

    return [promptMessage]


def getSeniorDevGptTestPromptRaw():
    return testUserPrompt


def getFeedbackFromAgentPromptMessage(stepIndex, agentName, agentCommand, agentAnswer):
    prompt = f"""Step index {stepIndex}. You asked `{agentName}` to execute the following command: `{agentCommand}`, and he responded with `{agentAnswer}`.
What is the next agent command you want to execute?\nRespond using the same template as before:
`stepIndex ::: agentName - agentCommand`"""

    promptMessage = {"role": "user", "content": prompt}

    return promptMessage
