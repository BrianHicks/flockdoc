"functions for handling code"
from itertools import groupby
from markdown import markdown

LANGUAGES = {
    "py": "#",
    "js": "//",
}

def detect_filetype(filename):
    'detect a filetype to get comments'
    for ext in reversed(filename.split('.')):
        if ext in LANGUAGES:
            return ext

    raise ValueError('Cannot handle "%s". Unknown filetype' % filename)

def segment_lines(source, comment):
    'segment lines into groups of comment and code'
    groups = groupby(
        source.strip().split('\n'),
        lambda line: 'comment' if line.strip().startswith(comment) else 'code',
    )
    for category, group in groups:
        yield category, '\n'.join(list(group))
