# PyMDc
Simple Python MarkDown Console reader

# Usage
``python3 pymdc.py README.md --no-clear --casual-print --show-raw`` will:
* won't clear the console (by default it clears the console)
* print the file name
* will print and finish the script without waiting for user input
* show-raw - will show formatted text with escape codes

# Why input is the default option?
For me it feels more natural to not see command line prompt before I end reading the file.

If you don't like it, you may use ``--casual-print`` option

# Help
For more info use ``pymdc.py --help``

# Roadmap
- [ ] Open as ``app``, e.g. like vi or nano
- [ ] Set better colors for heading
- [ ] Handle tables
- [ ] Add more file metadata
- [ ] release to PyPi
- [ ] Add disclaimer handling
- [ ] Add Search

# Issues
- [ ] Italic and Bold that start of end line don't work
- [ ] Full-line comments leave empty line
- [ ] Multiline comments not supported yet
