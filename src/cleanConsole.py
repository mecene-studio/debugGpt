from colorama import Fore, Style
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

code = """
def hello_world():
    print('Hello, World!')

hello_world()
"""

# Use Pygments to highlight the code
highlighted_code = highlight(code, PythonLexer(), TerminalFormatter())

# Use Colorama to print it in color
print(Fore.GREEN + highlighted_code + Style.RESET_ALL)
