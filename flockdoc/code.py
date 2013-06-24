"functions for handling code"
from markdown import markdown

LANGUAGES = {
    "py": { "single": "#", "multi": ("\"\"\"", "\"\"\"") },
    "js": { "single": "//", "multi": ("/*", "*/") }
}

def detect_filetype(filename):
    for ext in reversed(filename.split('.')):
        if ext in LANGUAGES:
            return ext

    raise ValueError('Cannot handle "%s". Unknown filetype' % filename)

detect_lines = None
