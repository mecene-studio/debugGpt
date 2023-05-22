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

    try:
        with open(path, "w") as f:
            f.write(content)

        answer = "File written successfully to: test-app/" + filename

        return answer

    except FileNotFoundError:
        answer = "File not found: " + filename

        return answer
