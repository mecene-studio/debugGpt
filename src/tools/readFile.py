from lib.getPath import getPathFromTestApp, getPathFromWorkspace
from tools.runShell import getErrorsFromFile


def readFile(filename: str):
    path = getPathFromWorkspace(filename)

    return readFileFullPath(path)


def readFileFromTestApp(filename: str):
    extension = filename.split(".")[-1]
    print("extension", extension)

    if extension == "tsx":
        return readCodeFile(filename)

    path = getPathFromTestApp(filename)
    return readFileFullPath(path, filename)


def readCodeFile(filename: str):
    # extension = filename.split(".")[-1]
    # print("extension", extension)
    path = getPathFromTestApp(filename)

    content = readFileFullPath(path, filename)

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


def readFileFullPath(pathToFile: str, originalFilename=None):
    try:
        with open(pathToFile, "r") as f:
            content = f.read()

        return content

    except FileNotFoundError:
        # print("File not found: ", pathToFile)
        if originalFilename:
            return "File not found: " + originalFilename
        return "File not found: " + pathToFile
