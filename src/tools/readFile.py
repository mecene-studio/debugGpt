from lib.getPath import getPathFromTestApp, getPathFromWorkspace
from tools.runShell import getErrorsFromFile


def readFile(filename: str):
    path = getPathFromWorkspace(filename)

    return readFileFullPath(path)


def readFileFromTestApp(filename: str):
    extension = filename.split(".")[-1]

    if extension == "tsx":
        return readCodeFile(filename)

    try:
        path = getPathFromTestApp(filename)
        return readFileFullPath(path)
    except FileNotFoundError:
        return "ERROR: File not found: " + filename


def readCodeFile(filename: str):
    # extension = filename.split(".")[-1]
    # print("extension", extension)
    path = getPathFromTestApp(filename)

    try:
        content = readFileFullPath(path)
        print("content temp:", content)
    except FileNotFoundError:
        return "ERROR: File not found: " + filename

    # add linenumber) to each line
    lines = content.split("\n")
    linesWithLineNumbers = []
    for i, line in enumerate(lines):
        linesWithLineNumbers.append(str(i + 1) + ") " + line + "\n")

    content = "".join(linesWithLineNumbers)

    errors = getErrorsFromFile(filename)

    output = f"""FILE:
     
{filename}

CONTENT:

{content}
    
ERRORS:

{errors}

"""

    return output


def readFileFullPath(pathToFile: str):
    with open(pathToFile, "r") as f:
        content = f.read()

    return content
