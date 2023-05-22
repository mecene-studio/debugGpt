from tools.executeTool import runShell
from agents.utils.parseToolUserAnswer import parseToolUserAnswer
from tools.moveFile import moveFileFromTestApp
from tools.readFile import readFile
from tools.searchGoogle import searchGoggleCustom, searchGoggleLangChain
from tools.stackOverflow import getAnswersForStackOverflowPost, searchStackOverflow
from tools.writeFile import writeFileToWorkspace
from tools.listFiles import listFilesFromTestApp


def testWriteFile():
    print("Testing WriteFile:")

    content = """THIS is a file
    
    with multiple lines"""

    filename = "test.txt"

    writeFileToWorkspace(filename, content)


def testListFiles():
    print("Testing ListFiles:")

    tree = listFilesFromTestApp()
    print("tree\n", tree)


def testSearch():
    query = "Stackoverflow: 'Next.js Module not found: Can't resolve'"
    results = searchGoggleCustom(query)
    print("results\n", results)


def testReadFile():
    filename = "test.txt"
    content = readFile(filename)
    print("content\n", content)


def testParseDebugGptMessage():
    message = """writeFile(components/LandingPage.module.scss, ```$color-primary: #0070f3;
$color-secondary: #ff0080;
$color-white: #ffffff;
$color-black: #000000;

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: $color-primary;
}

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
}

.title {
  font-size: 3rem;
  font-weight: 700;
  color: $color-white;
  margin-bottom: 2rem;
}

.subtitle {
  font-size: 1.5rem;
  font-weight: 400;
  color: $color-white;
  margin-bottom: 3rem;
}

.button {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
  color: $color-primary;
  background-color: $color-white;
  border: none;
  border-radius: 50px;
  padding: 1rem 2rem;
  cursor: pointer;
  transition: all 0.2s ease-in-out;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.2);
  }
}

.icon {
  margin-left: 1rem;
  font-size: 2rem;
}

.canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
``` )"""
    functionName, arguments = parseToolUserAnswer(message)
    print("functionName\n", functionName)
    # print("arguments\n", arguments)
    for argument in arguments:
        print("argument\n", argument)


def testRunShell():
    command = "npm run build"
    output = runShell(command)
    print(
        "\n\n\n\n######################### output:\n",
        output + "\n#########################",
    )


def testStackOverflow():
    query = "Next.js Module not found: Can't resolve"
    # postId = "44439205"
    # results = getAnswersForStackOverflowPost(postId)
    # print("results\n", results)

    answer = searchStackOverflow(query)
    print("answer\n", answer)


def testMoveFile():
    file1 = "components/Header.tsx"
    file2 = "components/Header/Header.tsx"
    answer = moveFileFromTestApp(file1, file2)
    print("answer\n", answer)


if __name__ == "__main__":
    print("testTools.py")
    testMoveFile()
