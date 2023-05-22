import os
from lib.getPath import getPathFromTestApp


def moveFileFromTestApp(oldPathRelative: str, newPathRelative: str):
    oldPath = getPathFromTestApp(oldPathRelative)
    newPath = getPathFromTestApp(newPathRelative)

    try:
        with open(oldPath, "r") as f:
            content = f.read()
            # delete the file

    except FileNotFoundError as e:
        print("File not found: ", e)
        return "File not found: " + oldPathRelative

    try:
        with open(newPath, "w") as f:
            f.write(content)

    except FileNotFoundError as e:
        print("File not found: ", e)
        return "File not found: " + newPathRelative

    os.remove(oldPath)

    return "File moved successfully to: " + newPathRelative
