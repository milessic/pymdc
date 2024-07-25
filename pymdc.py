r"Miłosz Jura, version 1.0"
# TODO add new repo and set it up
import sys
import os
import re
from pathlib import Path
class Colors:
    # Colors
        VIOLET = '\033[95m'
        DIMMED= '\033[90m'
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
    # Classes
        FAIL = '\033[91m'
        WARNING = '\033[93m'
    # Other formatting
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        ENDC = '\033[0m'

if __name__ == "__main__":
    help_text = """PyMDc, simple tool to display MD files.
    pymdc.py {FILE} {ARGUMENTS}
    --help         - you know 8)
    --no-clear     - won't clear the console before printing contents
    --show-raw     - prints raw output before everything else
    --no-filename  - won't print filename at the beggining
    --casual-print - won't block with input, and only display
    """
    show_raw = "--show-raw" in sys.argv[1:]
    # read first argument and treat it as file_name
    try:
        file_name = Path(sys.argv[1]).name
    except IndexError:
        print(help_text)
        exit()
    
    # print help if help was called
    if "--help" in sys.argv:
        print(help_text)
        exit()

    # clear the console or not, depending on settings
    if not "--no-clear" in sys.argv:
        os.system("clear") 
    
    # open file 
    file_name = f"{sys.argv[1]}"
    try:
        with open(file_name, "r") as f:
            file_lines = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(Colors.BOLD + Colors.FAIL + f"File '{file_name}' not found!\nPlease ensure file name or path is correct" + Colors.ENDC)
    
    # clear empty lines from file end
    while repr(file_lines[-1]) == "'\\n'":
        file_lines.pop()
    file = ""
    
    # code_started will be used to the text formatted using ```
    code_started = False
    # iterate through read file
    for l in file_lines:
        # handle ``` code blocks
        if not code_started and l.startswith("```"):
            line = Colors.YELLOW+ l
            code_started = True
            file += line
            continue
    
        if code_started:
            line = l
            if l.startswith("```"):
                line = l + Colors.ENDC
                code_started = False

        # handle other text 
        else:
            l = re.sub(r"\s((?<!`)``(?!`))", Colors.DIMMED + " ``", l) 
            l = re.sub(r"((?<=\S)(?<!`)``(?!`))", "``"+ Colors.ENDC, l)
            if l.startswith("###"):
                line = Colors.CYAN + l + Colors.ENDC
            elif l.startswith("##"):
                line = Colors.GREEN+ l + Colors.ENDC
            elif l.startswith("#"):
                line = Colors.BLUE + l + Colors.ENDC
            elif l.startswith("- ["):
                line = l.replace("[ ]", Colors.BLUE+ "[ ]" + Colors.ENDC).replace("[x]", Colors.GREEN+ "[x]" + Colors.ENDC)
            else:
                line = l
        file += line

        # print raw line if needed
        if show_raw:
            print(repr(line))

    # display file name
    if not "--no-filename" in sys.argv:
        print(f"{Colors.BOLD}=== File: {file_name}{Colors.ENDC}")
    # display file contents in one ways
    if "--casual-print" in sys.argv:
        print(file)
    else:
        input(file)

