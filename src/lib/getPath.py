import os


def getPathFromWorkspace(filename: str):
    rootPath = getRoothPath() + "workspace"

    path = os.path.join(rootPath, filename)

    return path


def getWorkspacePath():
    rootPath = getRoothPath() + "workspace"

    return rootPath


def getRoothPath():
    currentFile = os.path.abspath(__file__)

    # stop at src
    rootPath = currentFile.split("src")[0]

    return rootPath


def getPathFromComponents(filename: str):
    rootPath = getRoothPath() + "test-app/components"

    path = os.path.join(rootPath, filename)

    return path


def getTestAppPath():
    rootPath = getRoothPath() + "test-app"

    return rootPath


def getPathFromTestApp(filename: str):
    rootPath = getRoothPath() + "test-app"

    path = os.path.join(rootPath, filename)

    return path
