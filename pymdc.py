r"Miłosz Jura, version 1.0"
import curses
import textwrap
import sys
import os
import re
from pathlib import Path

class FileNameNotProvided(Exception):
    def __init__(self, *args, **kwargs):
        self.args = ("FileNameNotProvided: Filename has to provided either when initializing or when calling for read",)
        super().__init__(*args, **kwargs)

# Define colors using curses
class Colors:
    def __init__(self, stdscr):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # BOLD
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # FAIL
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # YELLOW
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)   # BLUE_LIGHT
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)  # GREEN_LIGHT
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)# VIOLET
        curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)    # RED
        curses.init_pair(8, curses.COLOR_CYAN, curses.COLOR_BLACK)   # CYAN
        curses.init_pair(9, curses.COLOR_GREEN, curses.COLOR_BLACK)  # GREEN
        curses.init_pair(10, curses.COLOR_BLUE, curses.COLOR_BLACK)  # BLUE
        curses.init_pair(11, curses.COLOR_WHITE, curses.COLOR_BLACK) # DIMMED

        self.BOLD = curses.color_pair(1) | curses.A_BOLD
        self.ITALIC= curses.color_pair(1) | curses.A_ITALIC
        self.FAIL = curses.color_pair(2)
        self.YELLOW = curses.color_pair(3)
        self.WARNING = curses.color_pair(3)
        self.BLUE_LIGHT = curses.color_pair(4)
        self.GREEN_LIGHT = curses.color_pair(5)
        self.VIOLET = curses.color_pair(6)
        self.RED = curses.color_pair(7)
        self.CYAN = curses.color_pair(8)
        self.GREEN = curses.color_pair(9)
        self.BLUE = curses.color_pair(10)
        self.DIMMED = curses.color_pair(11)

        self.ENDC = curses.A_NORMAL

class Colors_c:
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

class PyMdC:
    def __init__(self, filename:str|None = None, cat_mode:bool=False):
        self.filename = filename
        self.cat_mode = cat_mode
        self.help_text = """PyMDc, simple tool to display MD files.
        pymdc.py {FILE} {ARGUMENTS}
        --help         - you know 8)
        --no-clear     - won't clear the console before printing contents
        --show-raw     - prints raw output before everything else
        --no-filename  - won't print filename at the beggining
        --casual-print - won't block with input, and only display
        """

    def start(self, filename:str | None = None):
        if filename is None:
            if self.filename is None:
                raise FileNameNotProvided
            else:
                filename = self.filename
        else:
            self.filename = filename
        if self.cat_mode:
            self._cat_print()
        else:
            self._open_reader()
        # print help if help was called
        if "--help" in sys.argv:
            print(self.help_text)
            exit()

    def _open_reader(self):
        curses.wrapper(self._app)

    def _app(self, stdscr):
        file_content = self._convert_file_stdscr(stdscr, filename)
        stdscr.clear()
        for color, line in file_content:
            if color:
                stdscr.addstr(line, color)
            else:
                stdscr.addstr(line)
        stdscr.refresh()
        stdscr.getkey()
        return
        # TODO colors implementation
        content = self._convert_file_stdscr(stdscr, filename)
        curses.start_color()
        curses.use_default_colors()
        rows, cols = stdscr.getmaxyx()
        #lines = content.splitlines()
        #wrapped_content = [j for i in lines for j in textwrap.wrap(i, width=cols-2)]
        wrapped_content = content
        stdscr.clear()
        i = 0
        with open("log","a") as f:
            f.write(f"{wrapped_content}\n")
        for l in wrapped_content:
            stdscr.addstr(i, 0, l)
            i+=1
        stdscr.refresh()
        stdscr.getkey()


    def _cat_print(self):
        content = self._convert_file_cat(filename)
        # clear the console or not, depending on settings
        if not "--no-clear" in sys.argv:
            os.system("clear") 
        # display file contents in one ways
        if not "--no-filename" in sys.argv:
            print(f"{Colors_c.BOLD}=== File: {filename}{Colors_c.ENDC}")
        if "--casual-print" in sys.argv:
            print(content)
        else:
            input(content)
        pass

    def _convert_file_cat(self, filename) -> str:
        show_raw = "--show-raw" in sys.argv[1:]
    
        
        # open file 
        try:
            with open(filename, "r") as f:
                file_lines = f.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(Colors_c.BOLD + Colors_c.FAIL + f"File '{filename}' not found!\nPlease ensure file name or path is correct" + Colors_c.ENDC)
        
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
                line = Colors_c.YELLOW+ l
                code_started = True
                file += line
                continue
        
            if code_started:
                line = l
                if l.startswith("```"):
                    line = l + Colors_c.ENDC
                    code_started = False
    
            if not alert_started and l.startswith("> ["):
                if "[!WARNING]" in l:
                    line =  Colors_c.WARNING + l
                elif "[!NOTE]" in l:
                    line = Colors_c.BLUE_LIGHT + l
                elif "[!TIP]" in l:
                    line = Colors_c.GREEN_LIGHT + l
                elif "[!IMPORTANT]" in l:
                    line = Colors_c.VIOLET + l
                elif "[!CAUTION]" in l:
                    line = Colors_c.RED + l
                else:
                    line = l
                alert_started = True
                file += line
                continue
            if alert_started:
                # check if next line is alert as well
                if not file_lines[index+1].startswith("> "):
                    line = l + Colors_c.ENDC
                    alert_started = False
                    file += line
                    continue
            # handle other text 
            else:
                l = re.sub(r"\s((?<!`)``(?!`))", Colors_c.DIMMED + " ``", l) 
                l = re.sub(r"((?<=\S)(?<!`)``(?!`))", "``"+ Colors_c.ENDC, l)
                if l.startswith("###"):
                    line = Colors_c.CYAN + l + Colors_c.ENDC
                elif l.startswith("##"):
                    line = Colors_c.GREEN+ l + Colors_c.ENDC
                elif l.startswith("#"):
                    line = Colors_c.BLUE + l + Colors_c.ENDC
                elif l.startswith("- ["):
                    line = l.replace("[ ]", Colors_c.BLUE+ "[ ]" + Colors_c.ENDC).replace("[x]", Colors_c.GREEN+ "[x]" + Colors_c.ENDC)
                elif l.startswith("  - ["):
                    line = l.replace("[ ]", Colors_c.BLUE_LIGHT+ "[ ]" + Colors_c.ENDC).replace("[x]", Colors_c.GREEN_LIGHT+ "[x]" + Colors_c.ENDC)
                elif "    - [" in l: # TODO do it better, "    - [" doesnt work for some reason
                    line = l.replace("[ ]", Colors_c.BLUE_LIGHT+ "[ ]" + Colors_c.ENDC).replace("[x]", Colors_c.GREEN_LIGHT+ "[x]" + Colors_c.ENDC)
                else:
                    line = l
                # comment
                line = re.sub(r"<!--[\s\S]*?-->", "", line)
                # bold
                """
                # FIXME start add regex 
                if line.startswith("__") or line.startswith("**"):
                    line = line.replace("**", " " + Colors_c.BOLD)
                    line = line.replace("__", Colors_c.ENDC + " ")
                if line.endswith("__") or line.endswith("**"):
                    line = line.replace("__", Colors_c.ENDC + " ")
                    line = line.replace("**", Colors_c.ENDC + " ")
                if line.startswith("_ _") or line.startswith("* *"):
                    line = line.replace("* *", " " + Colors_c.ITALIC)
                    line = line.replace("_ _", " " + Colors_c.ITALIC)
                if line.endswith("_ _") or line.endswith("* *"):
                    line = line.replace("_ _", Colors_c.ENDC + " ")
                    line = line.replace("* *", Colors_c.ENDC + " ")
                # FIXME end
                """
    
    
                line = line.replace(" __", " " + Colors_c.BOLD)
                line = line.replace("__ ", Colors_c.ENDC + " ")
                line = line.replace(" **", " " + Colors_c.BOLD)
                line = line.replace("** ", Colors_c.ENDC + " ")
    
                line = line.replace(" _ _", " " + Colors_c.ITALIC)
                line = line.replace("_ _ ", Colors_c.ENDC + " ")
                line = line.replace(" * *", " " + Colors_c.ITALIC)
                line = line.replace("* * ", Colors_c.ENDC + " ")
            file += line
            # print raw line if needed
            #if show_raw:
            #    print(repr(line))
        return file
    def _convert_file_stdscr(self, stdscr, filename):
    #def _convert_file_cat(filename):
        colors = Colors(stdscr)
        show_raw = "--show-raw" in sys.argv[1:]
        
        # open file 
        try:
            with open(filename, "r") as f:
                file_lines = f.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"{colors.BOLD}{colors.FAIL}File '{filename}' not found!\nPlease ensure file name or path is correct{colors.ENDC}")
        
        # clear empty lines from file end
        while repr(file_lines[-1]) == "'\\n'":
            file_lines.pop()
        
        file = []
        code_started = False
        alert_started = False
        index = -1

        for l in file_lines:
            index += 1

            # handle ``` code blocks
            if not code_started and l.startswith("```"):
                line = (colors.YELLOW, l)
                code_started = True
                file.append(line)
                continue

            if code_started:
                if l.startswith("```"):
                    line = (colors.ENDC, l)
                    code_started = False
                else:
                    line = (colors.YELLOW, l)
                file.append(line)
                continue

            if not alert_started and l.startswith("> ["):
                if "[!WARNING]" in l:
                    color = colors.WARNING
                elif "[!NOTE]" in l:
                    color = colors.BLUE_LIGHT
                elif "[!TIP]" in l:
                    color = colors.GREEN_LIGHT
                elif "[!IMPORTANT]" in l:
                    color = colors.VIOLET
                elif "[!CAUTION]" in l:
                    color = colors.RED
                else:
                    color = colors.ENDC
                line = (color, l)
                alert_started = True
                file.append(line)
                continue
            
            if alert_started:
                if not file_lines[index+1].startswith("> "):
                    line = (colors.ENDC, l)
                    alert_started = False
                    file.append(line)
                    continue

            l = re.sub(r"\s((?<!`)``(?!`))", f" {colors.DIMMED} ``", l) 
            l = re.sub(r"((?<=\S)(?<!`)``(?!`))", f"``{colors.ENDC}", l)
            if l.startswith("###"):
                line = (colors.CYAN, l)
            elif l.startswith("##"):
                line = (colors.GREEN, l)
            elif l.startswith("#"):
                line = (colors.BLUE, l)
            elif l.startswith("- ["):
                line = (None, l.replace("[ ]", f"{colors.BLUE}[ ]{colors.ENDC}").replace("[x]", f"{colors.GREEN}[x]{colors.ENDC}"))
            elif l.startswith("  - ["):
                line = (None, l.replace("[ ]", f"{colors.BLUE_LIGHT}[ ]{colors.ENDC}").replace("[x]", f"{colors.GREEN_LIGHT}[x]{colors.ENDC}"))
            else:
                line = (None, l)
            line = re.sub(r"<!--[\s\S]*?-->", "", line[1])
            line = line.replace(" __", f" {colors.BOLD}")
            line = line.replace("__ ", f"{colors.ENDC} ")
            line = line.replace(" **", f" {colors.BOLD}")
            line = line.replace("** ", f"{colors.ENDC} ")
            line = line.replace(" _ _", f" {colors.ITALIC}")
            line = line.replace("_ _ ", f"{colors.ENDC} ")
            line = line.replace(" * *", f" {colors.ITALIC}")
            line = line.replace("* * ", f"{colors.ENDC} ")
            file.append((None, line))

        return file

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    cat_mode = True if "--cat" in sys.argv else True # TODO change after reader implementation
    cat_mode = False if "-r" in sys.argv else cat_mode
    app = PyMdC(
            cat_mode=cat_mode
                )
    app.start(sys.argv[1])
