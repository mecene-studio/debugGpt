import os
import subprocess
import time
from lib.getPath import getTestAppPath


def runShellPopen(commandRaw: str):
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
    createScssTypesCommand = "npx typed-scss-modules **/*.scss"
    answerTypes = runShell(createScssTypesCommand)

    # compileTscCommand = f"npx tsc {filename} --jsx react --noEmit --esModuleInterop --allowArbitraryExtensions"

    debugCommand = "node ignore/debug.js " + filename

    if allFiles:
        debugCommand = f"node ignore/debug.js {BASEFILE} --all"

    rawAnswer = runShell(debugCommand)

    # print("rawAnswer: ", rawAnswer)

    trash, answer = rawAnswer.split("Error #", 1)
    answer = "Error #" + answer

    return answer
