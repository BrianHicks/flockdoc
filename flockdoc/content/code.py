"functions for handling code"
from itertools import groupby
from markdown import markdown

from ..renderer import env

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

    def segment_lines(self, include_type=False):
        'segment lines into groups of comment and code'
        comment = self.LANGUAGES[self.filetype]

        groups = groupby(
            self.content.strip().split('\n'),
            lambda line: 'comment' if line.strip().startswith(comment) else 'code',
        )

        for category, group in groups:
            if include_type:
                yield category, '\n'.join(group)
            else:
                yield '\n'.join(group)

    def render(self, template='content/code.html'):
        'render code content'
        segments = list(self.segment_lines())
        sections = [
            {
                'markdown': markdown('\n'.join([
                    line.lstrip(self.LANGUAGES[self.filetype])
                    for line in segments[i].split('\n')
                ])),
                'code': '' if i + 1 >= len(segments) else segments[i+1]
            }
            for i in range(0, len(segments), 2)
        ]

        return env.get_template('content/code.html').render(
            sections=sections,
            filename=self.filename,
        )
