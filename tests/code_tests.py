"tests for flockdoc/code.py"
from flockdoc.code import CodePage

def test_codepage_init():
    x = CodePage('test.py', 'test')
    assert x.filename == 'test.py', x.filename
    assert x.content == 'test', x.content
    assert x.filetype == 'py', x.filetype

def test_detect_filetype_works():
    'test detect_filetype'
    cases = {
        "test.py": "py",
        "test.py.md": "py",
        "test.js": "js",
        "test.js.md": "js"
    }

    def check(i, o):
        assert i.filetype == o, '%r != %r (got %r)' % (i, o, i.filetype)

    for i, o in cases.items():
        yield check, CodePage(i, ''), o

def test_detect_filetype_fails():
    'detect_filetype fails when given unknown input'
    try:
        CodePage('what.q', '')
        assert False, "detect_filetype failed to fail at detecting 'what.q'"
    except ValueError as e:
        assert e.message == 'Cannot handle "what.q". Unknown filetype.', e.message

def test_segment_lines():
    'test segment_lines'
    cases = {
        "# test\n1": [('comment', '# test'), ('code', '1')],
        "# test\n# test\n1": [('comment', '# test\n# test'), ('code', '1')],
        "# test\n1\n# test": [('comment', '# test'), ('code', '1'), ('comment', '# test')],
    }
    
    def check(i, o):
        actual = list(i.segment_lines())
        assert actual == o, '%r != %r (got %r)' % (i, o, actual)

    for i, o in cases.items():
        yield check, CodePage('test.py', i), o
