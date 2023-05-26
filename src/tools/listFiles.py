# get a tree of files on the workspace
import os

from lib.getPath import getTestAppPath, getWorkspacePath


def listFilesFromWorkspace():
    path = getWorkspacePath()

    return listFilesFromPath(path)


ignoreList = [
    "test-app",
    ".next",
    "node_modules",
]


def listFilesFromPathTabs(path):
    treeString = ""

    print("path", path)
    # walk the directory recursively, adding a tab for each level but ignore what's in the ignoreList
    for root, dirs, files in os.walk(path):
        # remove the first directory from the path
        # print("root", root)
        dirs[:] = [d for d in dirs if d not in ignoreList]

        level = root.replace(path, "").count(os.sep)
        indent = "\t" * (level - 1)
        dirString = os.path.basename(root)
        # print("dirString", dirString)
        treeString += "{}{}/\n".format(indent, dirString)
        subindent = "\t" * (level)
        for f in files:
            treeString += "{}{}\n".format(subindent, f)

    # remove first line from treeString
    treeString = treeString.split("\n", 1)[1]
    return treeString


def listFilesFromPath(path):
    treeString = ""

    # print("path", path)
    # walk the directory recursively, adding a tab for each level but ignore what's in the ignoreList
    for root, dirs, files in os.walk(path):
        # remove the first directory from the path
        # print("root", root)
        dirs[:] = [d for d in dirs if d not in ignoreList]

        level = root.replace(path, "")

        if "ignore" in level:
            continue
        # indent = "\t" * (level - 1)
        # dirString = os.path.basename(root)
        # # print("dirString", dirString)
        # treeString += "{}{}/\n".format(indent, dirString)
        # subindent = "\t" * (level)
        for f in files:
            if ".d.ts" in f:
                continue
            filePath = level + "/" + f + "\n"
            treeString += filePath[1:]

    # remove first line from treeString
    treeString = treeString.split("\n", 1)[1]
    return treeString


def listFilesFromTestApp():
    path = getTestAppPath()

    return listFilesFromPath(path)
