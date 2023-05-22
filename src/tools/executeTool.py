from tools.listFiles import listFilesFromTestApp
from tools.moveFile import moveFileFromTestApp
from tools.readFile import readFileFromTestApp
from tools.runShell import runShell
from tools.stackOverflow import searchStackOverflow
from tools.writeFile import writeFileToTestApp


def executeTool(functionName, arguments):
    if functionName == "runCommand":
        return runShell(arguments[0])
    elif functionName == "readFile":
        return readFileFromTestApp(arguments[0])
    elif functionName == "listFiles":
        return listFilesFromTestApp()
    elif functionName == "moveFile":
        return moveFileFromTestApp(arguments[0], arguments[1])
    elif functionName == "askStackOverflow":
        return searchStackOverflow(arguments[0])
    elif functionName == "writeFile":
        return writeFileToTestApp(arguments[0], arguments[1].replace("```", ""))
    elif functionName == "endDebugging":
        return "Debugging ended"
    else:
        return "INTERNAL ERROR: functionName not recognized"
