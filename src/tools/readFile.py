import numpy
from lib.getPath import getPathFromTestApp, getPathFromWorkspace
from tools.listFiles import listFilesFromTestApp
from tools.runShell import getErrorsFromFile, getErrorsFromScssFile


def readFile(filename: str):
    path = getPathFromWorkspace(filename)

    return readFileFullPath(path)


def levenshteinDistanceDP(token1, token2):
    distances = numpy.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2

    a = 0
    b = 0
    c = 0

    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if token1[t1 - 1] == token2[t2 - 1]:
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]

                if a <= b and a <= c:
                    distances[t1][t2] = a + 1
                elif b <= a and b <= c:
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    return distances[len(token1)][len(token2)]


def getClosestFile(filename: str):
    files = listFilesFromTestApp().split("\n")
    minDistance = 100000000000
    closestFile = "None"
    for file in files:
        dsitance = levenshteinDistanceDP(filename, file)
        print("file", file, "distance", dsitance)
        if dsitance < minDistance:
            minDistance = dsitance
            closestFile = file

    return closestFile


def readFileFromTestApp(filename: str):
    filename = filename.replace('"', "").replace("'", "")
    extension = filename.split(".")[-1]
    if extension == "tsx" or extension == "scss":
        return readCodeFile(filename)

    try:
        path = getPathFromTestApp(filename)
        return readFileFullPath(path)
    except FileNotFoundError:
        return f"ERROR: File not found: '{filename}'. Closest file: `{getClosestFile(filename)}`"


def readCodeFile(filename: str):
    # extension = filename.split(".")[-1]
    # print("extension", extension)
    path = getPathFromTestApp(filename)

    try:
        content = readFileFullPath(path)
    except FileNotFoundError:
        return f"ERROR: File not found: '{filename}'. Closest file: `{getClosestFile(filename)}`"

    # # add linenumber) to each line
    # lines = content.split("\n")
    # linesWithLineNumbers = []
    # for i, line in enumerate(lines):
    #     linesWithLineNumbers.append(str(i + 1) + ") " + line + "\n")

    # content = "".join(linesWithLineNumbers)

    # errors = getErrorsFromFile(filename)
    if filename.endswith(".tsx"):
        errors = getErrorsFromFile(filename)
    elif filename.endswith(".scss"):
        errors = getErrorsFromScssFile(filename)
    else:
        errors = ""

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
