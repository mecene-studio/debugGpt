tools = """
askStackOverflow(question) : get the first answer to the most similar question on stackoverflow
searchGoogle(query) : get the snippet of the first 3 results from google
runCommand(command) : command to execute in the shell
readFile(filename) : get the content of the file so you can see what the error is. You don't need to write to the file if you don't want to.
listFiles() : list the files in the workspace to know what files are available to read or write
writeFile(filename, ```content```) : write content in the file to fix the error. Always surround the content with backticks: ```content``` because the content can be multiline.
"""

# moveFile(filename, newfilename) : move the file to fix the error


system_init = (
    """
You are a Next.js / Typescript developer. You have to build the app successfully using `npm run build` and then fix any errors that comes up.
Do not use `npm run dev`.

In react, import components from files in the same folder using `import Component from './Component'` and not `import Component from './Component/Component.tsx'`.

You can use the following tools to debug the app and fix the errors:"""
    + tools
    + """You should only answer with the tool and nothing else.

Good Answer (good because it only uses the tool):
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
)


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


def getDebugGptPromptMessages():
    promptMessage = {"role": "system", "content": system_init}
    return [promptMessage]


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
