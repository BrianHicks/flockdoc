"functions for handling code"
from itertools import groupby
from markdown import markdown
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter

from . import Page
from ..renderer import env

class CodePage(object):
    LANGUAGES = {
        "py": "#",
        "js": "//",
        "php": "//",
        "rb": "#",
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

    def render(self, template='layouts/code.html'):
        'render code content, returning filename and content'
        segments = list(self.segment_lines())

        lexer = get_lexer_for_filename(self.filename)
        formatter = HtmlFormatter()

        sections = [
            {
                'markdown': markdown('\n'.join([
                    line.lstrip(self.LANGUAGES[self.filetype])
                    for line in segments[i].split('\n')
                ])),
                'code': highlight(
                    '' if i + 1 >= len(segments) else segments[i+1],
                    lexer, formatter
                )
            }
            for i in range(0, len(segments), 2)
        ]

        rendered = env.get_template(template).render(
            sections=sections,
            filename=self.filename
        )

        return self.filename + ".html", rendered
