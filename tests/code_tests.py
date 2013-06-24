"tests for flockdoc/code.py"
from flockdoc.code import detect_filetype, detect_lines

def test_detect_filetype_works():
    cases = {
        "test.py": "py",
        "test.py.md": "py",
        "test.js": "js",
        "test.js.md": "js"
    }

    def check(i, o):
        actual = detect_filetype(i)
        assert actual == o, '%r != %r (got %r)' % (i, o, actual)

    for i, o in cases.items():
        yield check, i, o

def test_detect_filetype_fails():
    'detect_filetype fails when given unknown input'
    try:
        detect_filetype('what.q')
        assert False, "detect_filetype failed to fail at detecting 'what.q'"
    except ValueError:
        pass
