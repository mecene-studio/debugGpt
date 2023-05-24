import agents.utils.basicprompts as p
from tools.listFiles import listFilesFromTestApp

system_init = """
Your name is debugGpt, you are a junior full-stack developper powered by chatGpt. 
Your goal is to debug a next.js application so that it builds properly.
You are a very good developer, and you know how to write clean, maintainable code.
You also are very good at finding errors in code, and you can fix them easily.
"""

reevaluateAtEachStep = """
The command will be executed by the tool you chose, and the result will be sent to you.
You will have to analyze the result, and reply with the next tool command.
"""


only_use = """
You must answer only with a tool and the arguments. You are not allowed to use anything else. No sentences, no words, no numbers, no symbols, no emojis, no nothing. 
These are your available tools:
"""

tools_list = """
1: searchGoogle ( query ) - to search the web for answers, not code specific
2: writeFile ( ``` content ``` ) - to write code in a file. Always use 3 backticks to write content in a file
3: readFile ( pathToFile ) - to read code from a file
4: listFiles (  ) - to list the files in the workspace to know what files are available to read or write
5: generateCode ( ) - to generate code using by giving a prompt to the GPT-3-5-turbo model
6: finishedanswer ( messageSummaryOfWhatHasBeenDoneToSendToUser  ) - to finish your answer and send it to the user
7: searchStackOverflow ( query ) - to search for answers to your coding questions
8: runShell ( command ) - to run a command in the terminal
"""

tool_reminder = """
Only answer with one tool at a time.
"""


good_n_bad_examples = """

Good Answer:
runShell ( npm run build )

Bad Answer ( bad because there is extra text ):
I would like to execute the readFile command to check the content of the LandingPage.tsx file.

Good Answer ( good because it only uses the tool ):
readFile( components/LandingPage.tsx )

Bad Answer ( bad because there is only 1 backtick instead of 3 ):
writeFile( components/LandingPage.tsx,`import React from "react";
import s from "./LandingPage.module.scss";

const LandingPage = () => {
  return (
    <div className={s.container}>
        <span>hello</span>
    </div>
  );
};

export default LandingPage;
` )

Good Answer (good because there are 3 backticks around the content):
writeFile( components/LandingPage.tsx,```import React from "react";
import s from "./LandingPage.module.scss";

const LandingPage = () => {
  return (
    <div className={s.container}>
        <span>hello</span>
    </div>
  );
};

export default LandingPage;
``` )

"""


remember_only_use = only_use + tools_list + tool_reminder


def getDebugGptPromptMessages():
    plannerPrompt = (
        system_init + reevaluateAtEachStep + remember_only_use + good_n_bad_examples
    )

    promptMessage = {"role": "system", "content": plannerPrompt}

    return [promptMessage]


def getDebugGptFileMessage():
    message = {
        "role": "system",
        "content": "These are the files in the project:\n" + listFilesFromTestApp(),
    }

    return message


def getFeedbackFromAgentPromptMessage(stepIndex, agentName, agentCommand, agentAnswer):
    prompt = f"""Step index {stepIndex}. You asked `{agentName}` to execute the following command: `{agentCommand}`, and he responded with `{agentAnswer}`.
What is the next command you want to execute?\nRespond using the same template as before:
` agentName ( agentArguments ) )`"""

    promptMessage = {"role": "user", "content": prompt}

    return promptMessage


def getFeedbackFromUserPrompt(feedback):
    prompt = f"""The user stopped you from running the command and gave you this feedback:
{feedback}

What is the next command you want to execute?
You can only answer with 1 tool and its arguments.
Respond using the same template as before:
toolName ( toolArguments ) 
"""
    return prompt


def getFeedbackFromCodeExecutionPrompt(command, output: str):
    # max length of output is 1000 characters
    output = output[-1000:]

    prompt = f"""your ran the command:{command} and it returned: 
```
{output} 
```
What is the next command you want to execute?
You can only answer with 1 tool and its arguments.
Respond using the same template as before:
toolName ( toolArguments ) 
"""

    return prompt
