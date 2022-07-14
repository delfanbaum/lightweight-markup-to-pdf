from lwm2pdf.process_docs import asciidoc_to_html, md_to_html
from unittest.mock import MagicMock, patch
import pytest


def test_md_to_html(tmpdir):
    """
    tests that the markdown converter function converts
    (does not test the actual markdown2 rendering)
    """

    fn = tmpdir / "file.md"
    with open(fn, 'w') as f:
        f.write("""# Hello world!
This "is" some _markdown_.""")

    result = md_to_html(fn)
    expected = """<h1 id="hello-world">Hello world!</h1>

<p>This &#8220;is&#8221; some <em>markdown</em>.</p>"""
    assert result.rstrip() == expected

