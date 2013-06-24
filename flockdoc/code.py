"functions for handling code"
from itertools import groupby
from markdown import markdown

class CodePage(object):
    LANGUAGES = {
        "py": "#",
        "js": "//",
    }

    def __init__(self, filename, content):
        self.filename, self.content = filename, content
        self.filetype = self.detect_filetype()

    def detect_filetype(self, filename=None):
        'detect a filetype to get comments'
        filename = filename or self.filename

        for ext in reversed(filename.split('.')):
            if ext in self.LANGUAGES:
                return ext

        raise ValueError('Cannot handle "%s". Unknown filetype.' % filename)

    def segment_lines(self):
        'segment lines into groups of comment and code'
        comment = self.LANGUAGES[self.filetype]

        groups = groupby(
            self.content.strip().split('\n'),
            lambda line: 'comment' if line.strip().startswith(comment) else 'code',
        )

        for category, group in groups:
            yield category, '\n'.join(list(group))
