import time
from agents.agent import DebugGpt
from agents.utils.debuggptprompt import getFeedbackFromCodeExecutionPrompt
from cleanConsole import resetConsoleColor, setConsoleColor


if __name__ == "__main__":
    # agent = DebugGpt()
    # agent.startLoop("debug the application")

    setConsoleColor("cyan")
    print("\n\n################## answer from", "debugGpt", ": \n")
    print(
        "We can now run the get bugs tool command to see if there are any more errors."
    )
    print("\n################## ")

    time.sleep(1)

    resetConsoleColor()
    print("WILL RUN COMMAND:", "getBugs")
    print("ARGUMENT", 0, ": ", "")

    time.sleep(1)

    print(
        "\nPress Enter to run, Type 'run -N' to run it for N iterations, Type 't' to tell agent to try again or type anything to send it as feedback:"
    )

    time.sleep(1)

    setConsoleColor("yellow")
    print("\n################## output from tool: \n")
    print("No errors found")
    resetConsoleColor()

    time.sleep(1)

    setConsoleColor("cyan")
    print("\n\n################## answer from", "debugGpt", ": \n")
    print(
        "The get bugs tool returned an empty list, which means that there are no more bugs in the application. We have successfully debugged the next.js application!"
    )
    print("\n################## ")

    time.sleep(1)
