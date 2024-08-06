r"Miłosz Jura, version 1.0"
import sys
import os
import re
from pathlib import Path
class Colors:
    # Colors
        VIOLET = '\033[95m'
        DIMMED= '\033[90m'
        BLUE = '\033[94m'
        BLUE_LIGHT = '\033[96m'
        BLUE_LIGHTER = '\033[96m'
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        GREEN_LIGHT = '\033[93m'
        GREEN_LIGHTER = '\033[93m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
    # Classes
        FAIL = '\033[91m'
        WARNING = '\033[93m'
    # Other formatting
        BOLD = '\033[1m'
        ITALIC = '\033[3m'
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
    alert_started = False
    comment_started = False
    index = -1
    # iterate through read file
    for l in file_lines:
        index += 1

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

        if not alert_started and l.startswith("> ["):
            if "[!WARNING]" in l:
                line =  Colors.WARNING + l
            elif "[!NOTE]" in l:
                line = Colors.BLUE_LIGHT + l
            elif "[!TIP]" in l:
                line = Colors.GREEN_LIGHT + l
            elif "[!IMPORTANT]" in l:
                line = Colors.VIOLET + l
            elif "[!CAUTION]" in l:
                line = Colors.RED + l
            else:
                line = l
            alert_started = True
            file += line
            continue
        if alert_started:
            # check if next line is alert as well
            if not file_lines[index+1].startswith("> "):
                line = l + Colors.ENDC
                alert_started = False
                file += line
                continue
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
            elif l.startswith("  - ["):
                line = l.replace("[ ]", Colors.BLUE_LIGHT+ "[ ]" + Colors.ENDC).replace("[x]", Colors.GREEN_LIGHT+ "[x]" + Colors.ENDC)
            elif "    - [" in l: # TODO do it better, "    - [" doesnt work for some reason
                line = l.replace("[ ]", Colors.BLUE_LIGHT+ "[ ]" + Colors.ENDC).replace("[x]", Colors.GREEN_LIGHT+ "[x]" + Colors.ENDC)
            else:
                line = l
            # comment
            line = re.sub(r"<!--[\s\S]*?-->", "", line)
            # bold
            """
            # FIXME start add regex 
            if line.startswith("__") or line.startswith("**"):
                line = line.replace("**", " " + Colors.BOLD)
                line = line.replace("__", Colors.ENDC + " ")
            if line.endswith("__") or line.endswith("**"):
                line = line.replace("__", Colors.ENDC + " ")
                line = line.replace("**", Colors.ENDC + " ")
            if line.startswith("_ _") or line.startswith("* *"):
                line = line.replace("* *", " " + Colors.ITALIC)
                line = line.replace("_ _", " " + Colors.ITALIC)
            if line.endswith("_ _") or line.endswith("* *"):
                line = line.replace("_ _", Colors.ENDC + " ")
                line = line.replace("* *", Colors.ENDC + " ")
            # FIXME end
            """


            line = line.replace(" __", " " + Colors.BOLD)
            line = line.replace("__ ", Colors.ENDC + " ")
            line = line.replace(" **", " " + Colors.BOLD)
            line = line.replace("** ", Colors.ENDC + " ")

            line = line.replace(" _ _", " " + Colors.ITALIC)
            line = line.replace("_ _ ", Colors.ENDC + " ")
            line = line.replace(" * *", " " + Colors.ITALIC)
            line = line.replace("* * ", Colors.ENDC + " ")
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

"""
