import os
from lib.getPath import (
    getPathFromComponents,
    getPathFromTestApp,
    getPathFromWorkspace,
)


def writeFileToWorkspace(filename: str, content: str):
    path = getPathFromWorkspace(filename)

    with open(path, "w") as f:
        f.write(content)
    print("File written successfully to", path)


def writeFileToComponents(filename: str, content: str):
    path = getPathFromComponents(filename)

    with open(path, "w") as f:
        f.write(content)

    answer = "File written successfully to: components/" + filename
    # print(answer)
    return answer


def writeFileToTestApp(filename: str, content: str):
    path = getPathFromTestApp(filename)

    # recursively create directories if they don't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)

    try:
        with open(path, "w") as f:
            f.write(content)

        answer = "File written successfully to: test-app/" + filename

        return answer

    except FileNotFoundError:
        answer = "File not found: " + filename

        return answer
