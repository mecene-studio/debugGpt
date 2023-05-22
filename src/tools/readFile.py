from lib.getPath import getPathFromTestApp, getPathFromWorkspace


def readFile(filename: str):
    path = getPathFromWorkspace(filename)

    return readFileFullPath(path)


def readFileFromTestApp(filename: str):
    path = getPathFromTestApp(filename)

    try:
        return readFileFullPath(path)

    except FileNotFoundError:
        # print("File not found: ", pathToFile)
        return "File not found: " + filename


def readFileFullPath(pathToFile: str):
    with open(pathToFile, "r") as f:
        content = f.read()

    return content
