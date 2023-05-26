import os
import re
import subprocess
import time
from lib.getPath import getTestAppPath


def runShellPopen(commandRaw: str):
    # if commandRaw starts and ends with a quote, remove them
    if commandRaw.startswith('"') and commandRaw.endswith('"'):
        commandRaw = commandRaw[1:-1]

    # Change directory to the desired folder
    folder_path = getTestAppPath()
    os.chdir(folder_path)

    # Define the command to run
    # command = ["npm", "run", "build"]
    command = commandRaw.split(" ")
    # print("command: ", command)

    maxExecutionTime = 10  # seconds

    # Run the command using subprocess with stdout and stderr as PIPE
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
    )

    print(
        "started process: ",
        process,
        "for ",
        maxExecutionTime,
        "seconds",
    )

    if process.stdout == None:
        print("process.stdout is None")
        return "INTERNAL ERROR: process.stdout is None"

    if process.stderr == None:
        print("process.stderr is None")
        return "INTERNAL ERROR: process.stderr is None"

    # print("reached while loop")

    shellOutput = ""

    startTime = time.time()

    # Read and print the output in real-time
    while True:
        # print("waiting for output")
        output = process.stdout.read()
        # print("waiting for error")
        error = process.stderr.read()

        if output:
            print(output.strip())
            shellOutput += output.strip() + "\n"

        if error:
            print(error.strip())
            shellOutput += error.strip() + "\n"

        # print("polling process:", process.returncode)

        # if output == "" and process.poll() is not None:
        #     break

        if time.time() - startTime > maxExecutionTime:
            print("maxExecutionTime reached")
            process.kill()
            break

    # Print the return code
    print("Process exited with return code:", process.returncode)

    # print("shellOutput: \n", shellOutput)

    return shellOutput


def runShell(commandRaw: str):
    # Change directory to the desired folder
    folder_path = getTestAppPath()
    os.chdir(folder_path)

    # Define the command to run
    # command = ["npm", "run", "build"]
    command = commandRaw.split(" ")
    # print("command: ", command)
    maxExecutionTime = 30  # seconds
    try:
        process = subprocess.run(
            command, timeout=maxExecutionTime, capture_output=True, text=True
        )

        answer = process.stdout + process.stderr

        return answer

    except subprocess.TimeoutExpired:
        return (
            "Max execution time "
            + str(maxExecutionTime)
            + " reached before command finished"
        )


BASEFILE = "app/page.tsx"


def getErrorsFromFile(filename, allFiles=False):
    # print("running sccss types")

    command = f"npx typed-scss-modules {filename} --logLevel error"
    if allFiles:
        command = "npx typed-scss-modules **/*.scss --ignore node_modules/**/*.scss --logLevel error"

    # print("command: ", command)
    answerTypes = runShell(command)
    # print("answerTypes: ", answerTypes)
    scssErrors = parseTypeAnswer(answerTypes)

    # print("answerTypes: ", answerTypes)

    # compileTscCommand = f"npx tsc {filename} --jsx react --noEmit --esModuleInterop --allowArbitraryExtensions"
    # print("running tsc")
    debugCommand = "node ignore/debug.js " + filename

    if allFiles:
        debugCommand = f"node ignore/debug.js {BASEFILE} --all"

    rawAnswer = runShell(debugCommand)

    # print("rawAnswer: ", rawAnswer)

    tsxErrors = ""
    key = "TSX ERROR #"
    if key in rawAnswer:
        trash, tsxErrorTemp = rawAnswer.split(key, 1)
        tsxErrors += key + tsxErrorTemp

    allErrors = scssErrors + "\n" + tsxErrors

    return allErrors


def parseTypeAnswer(answer: str):
    if "No files found." in answer:
        return ""

    lines = answer.split("\n")
    errors = []
    for line in lines:
        if line == "":
            continue
        if line.startswith("Found"):
            continue
        if line.startswith("[GENERATED TYPES]"):
            continue
        errors.append(line)

    # output = "\n".join(errors)
    output = ""

    for i, error in enumerate(errors):
        # get path and line number from error
        # error = "Function rgb is missing argument $green. (/Users/turcottep/dev/debugGpt/test-app/app/page.module.scss[199:7]"

        match = re.search(r"\((.*?)\[(.*?)\]\)", error)

        # error = error.split(")")[1].strip()
        if match:
            basePath = getTestAppPath() + "/"
            file_path = match.group(1)
            relative_file_path = file_path.replace(basePath, "")
            line_col = match.group(2)
            line_number = int(line_col.split(":")[0])

            partToRemove = f"({file_path}[{line_col}])"
            # print("partToRemove: ", partToRemove)
            error = error.replace(partToRemove, "")

            # print("File path:", file_path)
            # print("Line number:", line_number)

            output += f"SCSS ERROR #{i + 1} {relative_file_path} line {line_number }): {error}\n"
        else:
            output += f"SCSS ERROR #{i + 1} {error}\n"

    return output
