import time
from agents.agent import DebugGpt
from agents.utils.debuggptprompt import getFeedbackFromCodeExecutionPrompt
from cleanConsole import resetConsoleColor, setConsoleColor


if __name__ == "__main__":
    agent = DebugGpt()
    agent.startLoop("debug the application")
