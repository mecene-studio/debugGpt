import agents.utils.basicprompts as p

system_init = """
Your name is debugGpt and your are an experienced web developper. You are here to help the user debug his app and fix the errors.
You are a very good developer, and you know how to write clean, maintainable code. 
You are also able to come up with creative solutions to complex problems, so when the user gives you a command, you can find the best way to implement it. 

You have to build the app successfully using `npm run lint`, fix any issue, then `npm run build` and then fix any errors that comes up.
Your goal is to use the tools and agents provided to you to fix the errors and build the app successfully.
You have only fully answered the user's question when the app is built successfully and there are no errors.

"""


tools_list = """
askStackOverflow(question) : get the first answer to the most similar question on stackoverflow
runCommand(command) : command to execute in the shell
readFile(filename) : get the content of the file so you can see what the error is. You don't need to write to the file if you don't want to.
listFiles() : list the files in the workspace to know what files are available to read or write
finishedanswer() : use it when you have fully answered the user's question
"""

agents_list = """
0: completePlan - end the conversation once the plan is executed
1: searchGpt - give a query and receive a summary of the first results of a google search
2: juniorDevGpt - give a the summary of the code you want to generate, and the code will be generated
"""

reevaluateAtEachStep = """
Each command will be executed by the agent you chose, and the result will be sent to you.
You will have to analyze the result, and decide what to do next.
You could continue with the original plan, or change the plan based on the result."""

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


init = system_init + p.prompting_utils + p.using_steps + reevaluateAtEachStep
tools = p.tools_n_agents_init + tools_list + agents_list
tech = p.tech_stack + p.tech_rules


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
