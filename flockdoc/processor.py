import os

from .content.code import CodePage
from .content.markdown import MarkdownPage
from .content.static import StaticPage

def tree_files(root):
    'get files in a tree for the root'
    for root, dirs, files in os.walk(root):
        for filename in files:
            yield os.path.join(root, filename)

def render_all(source, destination):
    'render all the files in the tree'
    for filename in tree_files(source):
        cls = None

        if filename.endswith('.md'):
            cls = MarkdownPage
        elif 'code' in filename:
            cls = CodePage
        else:
            cls = StaticPage

        render_single(
            *cls(filename, open(filename, 'r').read()).render(),
            destination=destination
        )

def render_single(filename, content, destination):
    'render a single file out to a given destination'
    try:
        os.makedirs(os.path.join(destination, os.path.dirname(filename)))
    except OSError:  # already exists
        pass

    with open(os.path.join(destination, filename), 'w') as f:
        f.write(content)
        print "wrote %s" % os.path.join(destination, filename)
