from colorama import Fore, Style
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter


def printCode(code):
    # Use Pygments to highlight the code
    highlighted_code = highlight(code, PythonLexer(), TerminalFormatter())

    # Use Colorama to print it in color
    print(Fore.GREEN + highlighted_code + Style.RESET_ALL)


def resetConsoleColor():
    print(Style.RESET_ALL)


def setConsoleColor(color):
    if color == "green":
        print(Fore.GREEN)
    elif color == "red":
        print(Fore.RED)
    elif color == "blue":
        print(Fore.BLUE)
    elif color == "yellow":
        print(Fore.YELLOW)
    elif color == "magenta":
        print(Fore.MAGENTA)
    elif color == "cyan":
        print(Fore.CYAN)


def printUser(message):
    print(Fore.GREEN + message + Style.RESET_ALL)
