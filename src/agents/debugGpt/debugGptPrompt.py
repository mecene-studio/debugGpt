system_init = """
Your name is debugGpt and your are an experienced web developper. You are here to help the user debug his app and fix the errors.
You are a very good developer, and you know how to write clean, maintainable code. 
You are also able to come up with creative solutions to complex problems, so when the user gives you a command, you can find the best way to implement it. 

You have to build the app successfully using `npm run lint`, fix any issue, then `npm run build` and then fix any errors that comes up.
Your goal is to use the tools provided to debug the app and fix the errors

You have 2 states: planning and executing.


"""

prompting_utils = """
Anytime you see ||, you should assume the text inside the || is a variable, and you should replace it with the value of the variable.
"""


using_steps = """
When the user gives you a command, you have to analyze what he wants you to achieve, and create steps to answer it.
Thouroughly analyze the command to understand what the user wants to achieve.
If you feel like you are missing important information to achieve the command, you can ask the user for more information.
Otherwise, you should create steps to achieve the command.


When giving your answer, you should first list all the steps you are going to take in the format mentioned above.
Then you should execute the steps in order, writing "step index done" after each step is executed.
You have to wait for the "|step| |index| done" message of the index before you to execute the next step.
So if you have 3 steps, you should wait for the "step 1 done" message before executing the second step, and wait for the "step 2 done" message before executing the third step.

The goal of going through the steps instead of giving a direct answer is to be able to use the information learned in the previous steps to give a better answer in the next steps.
This is why you should wait for the "step index done" message before executing the next step because the next step might need the information from the previous step to be able to execute.
It is really important to do the steps in order, and to wait for the "step index done" message before executing the next step.
It is a crucial part of our system, and it is what makes our system so powerful.
You have to use the system we created to be able to give the best answer possible.

Once every step has been listed, then executed, you should finish your answer using the finishedanswer tool.

"""

tools_init = """
Each step should be using a tool, with the arguments to give to the tool, and the reason why you are using this tool.
index being the index of the step (1, 2, 3, ...), 
tool being the tool to use
arguments being the arguments to give to the tool (argument1, argument2, argument3, ...)
why being the reason why you are using this tool, which means what you are trying to achieve with this tool:

This is the format to use for a step using a tool:

|index|::: |tool|(|arguments|) - |why|

this is an example:
1::: readFile(components/LandingPage.tsx) - Because I want to check what components are used in the landing page, so I can know what components I need to create.

When giving your answer, you should list all the steps you are going to take in the format mentioned above.
You have access to these tools to help you achieve the user's command:
"""
tools_list = """
askStackOverflow(question) : get the first answer to the most similar question on stackoverflow
runCommand(command) : command to execute in the shell
readFile(filename) : get the content of the file so you can see what the error is. You don't need to write to the file if you don't want to.
listFiles() : list the files in the workspace to know what files are available to read or write
moveFile(filename, newfilename) : move the file to fix the error
writeFile(filename, ```content```) : write content in the file to fix the error. Always surround the content with backticks: ```content``` because the content can be multiline.
"""
tech_stack = """
To write web apps, use these technologies:
1: Next.js - as the frontend framework
2: React - as the frontend library
3: Typescript - as the language
4: Sass modules - as the styling language
5: Node.js - as the backend language
6: Prisma - as the ORM
7: Lucide - as the icon library
    """
tech_rules = """
Do not use `npm run dev`.
In react, import components from files in the same folder using `import Component from './Component'` and not `import Component from './Component/Component.tsx'`.
"""


good_n_bad_examples = """

You should only answer with the tool and nothing else.

Good Answer:
runCommand(npm run build)

Bad Answer (bad because there is extra text):
I would like to execute the readFile command to check the content of the LandingPage.tsx file.

Good Answer (good because it only uses the tool):
readFile(components/LandingPage.tsx)

Bad Answer (bad because there is only 1 backtick instead of 3):
writeFile(components/LandingPage.tsx,`import React from "react";
import s from "./LandingPage.module.scss";

const LandingPage = () => {
  return (
    <div className={s.container}>
        <span>hello</span>
    </div>
  );
};

export default LandingPage;
`)

Good Answer (good because there are 3 backticks around the content):
writeFile(components/LandingPage.tsx,```import React from "react";
import s from "./LandingPage.module.scss";

const LandingPage = () => {
  return (
    <div className={s.container}>
        <span>hello</span>
    </div>
  );
};

export default LandingPage;
```)
"""


example_console_command = """npm run build"""
example_console_output = """<w> [webpack.cache.PackFileCacheStrategy] Skipped not serializable cache item 'Compilation/modules|javascript/auto|/Users/turcottep/dev/tenxcoder/test-app/node_modules/next/dist/build/webpack/loaders/next-flight-css-loader.js!/Users/turcottep/dev/tenxcoder/test-app/node_modules/next/dist/build/webpack/loaders/css-loader/src/index.js??ruleSet[1].rules[4].oneOf[10].use[1]!/Users/turcottep/dev/tenxcoder/test-app/node_modules/next/dist/build/webpack/loaders/postcss-loader/src/index.js??ruleSet[1].rules[4].oneOf[10].use[2]!/Users/turcottep/dev/tenxcoder/test-app/node_modules/next/dist/build/webpack/loaders/resolve-url-loader/index.js??ruleSet[1].rules[4].oneOf[10].use[3]!/Users/turcottep/dev/tenxcoder/test-app/node_modules/next/dist/compiled/sass-loader/cjs.js??ruleSet[1].rules[4].oneOf[10].use[4]!/Users/turcottep/dev/tenxcoder/test-app/components/LandingPage.module.scss|sc_client': No serializer registered for SassError
> test-app@0.1.0 build
<w> while serializing webpack/lib/cache/PackFileCacheStrategy.PackContentItems -> webpack/lib/NormalModule -> webpack/lib/ModuleBuildError -> SassError
> next build
Failed to compile.


- info Creating an optimized production build...
./components/LandingPage.tsx
Module not found: Can't resolve 'canvas-confetti'

https://nextjs.org/docs/messages/module-not-found

Import trace for requested module:
./app/page.tsx

./components/LandingPage.tsx
Module not found: Can't resolve 'react-icons/ai'

https://nextjs.org/docs/messages/module-not-found

Import trace for requested module:
./app/page.tsx

./components/LandingPage.module.scss
SassError: Can't find stylesheet to import.
╷
1 │ @import "../../styles/variables.scss";
│         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
╵
components/LandingPage.module.scss 1:9  root stylesheet

Import trace for requested module:
./components/LandingPage.module.scss
./components/LandingPage.tsx
./app/page.tsx


> Build failed because of webpack errors
^CTraceback (most recent call last):
  File "/Users/turcottep/dev/tenxcoder/src/testAgents.py", line 42, in <module>
    startDebugGpt()
  File "/Users/turcottep/dev/tenxcoder/src/agents/debugGpt/debugGpt.py", line 30, in startDebugGpt
    output = process.stdout.readline()
  File "/Users/turcottep/miniconda3/lib/python3.10/codecs.py", line 319, in decode
    def decode(self, input, final=False):
KeyboardInterrupt

❯ python testAgents.py

<w> [webpack.cache.PackFileCacheStrategy] Skipped not serializable cache item 'Compilation/modules|javascript/auto|/Users/turcottep/dev/tenxcoder/test-app/node_modules/next/dist/build/webpack/loaders/next-flight-css-loader.js!/Users/turcottep/dev/tenxcoder/test-app/node_modules/next/dist/build/webpack/loaders/css-loader/src/index.js??ruleSet[1].rules[4].oneOf[10].use[1]!/Users/turcottep/dev/tenxcoder/test-app/node_modules/next/dist/build/webpack/loaders/postcss-loader/src/index.js??ruleSet[1].rules[4].oneOf[10].use[2]!/Users/turcottep/dev/tenxcoder/test-app/node_modules/next/dist/build/webpack/loaders/resolve-url-loader/index.js??ruleSet[1].rules[4].oneOf[10].use[3]!/Users/turcottep/dev/tenxcoder/test-app/node_modules/next/dist/compiled/sass-loader/cjs.js??ruleSet[1].rules[4].oneOf[10].use[4]!/Users/turcottep/dev/tenxcoder/test-app/components/LandingPage.module.scss|sc_client': No serializer registered for SassError
> test-app@0.1.0 build
<w> while serializing webpack/lib/cache/PackFileCacheStrategy.PackContentItems -> webpack/lib/NormalModule -> webpack/lib/ModuleBuildError -> SassError
> next build
Failed to compile.


- info Creating an optimized production build...
./components/LandingPage.tsx
Module not found: Can't resolve 'canvas-confetti'
Process exited with return code: 1
"""


def getDebugGptExampleCommand():
    return example_console_command


def getDebugGptExampleOutput():
    return example_console_output


init = system_init + prompting_utils + using_steps
tools = tools_init + tools_list
tech = tech_stack + tech_rules


def getDebugGptPromptMessages():
    promptMessage = [{"role": "system", "content": init + tools + tech}]
    return promptMessage


def getFeedbackFromCodeExecutionPrompt(command, output):
    # max length of output is 1000 characters
    output = output[-1000:]

    prompt = f"""You executed the command `{command}`.
this is the output 

```{output}
```

What is the next command you would like to execute?
Answer with the command only and nothing else.
"""

    return prompt


def getFeedbackFromUserPrompt(feedback):
    prompt = f"""The user stopped you from running the command and gave you this feedback:
{feedback}

What is the next command you would like to execute?
Answer with the command only and nothing else.
"""
    return prompt
