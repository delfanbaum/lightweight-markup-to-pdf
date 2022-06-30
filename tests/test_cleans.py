from lwm2pdf.clean_html import clean_footnotes, convert_quotes


class TestCleans:
    """
    Component tests for clean_html()
    """

    def test_convert_quotes(self):
        """
        Test to ensure we're not screwing up our quotes
        """
        start = """
        <div class="verseblock">
        <pre class="content">"On a summer's day"
        </pre>
        </div>
        <pre>"Not Converted"
        "Not Converted"</pre>
        "this" 'that' "the 'other'" <code>foo "bar"</code>
        """
        expected = """
        <div class="verseblock">
        <pre class="content">“On a summer's day”
        </pre>
        </div>
        <pre>"Not Converted"
        "Not Converted"</pre>
        “this” ‘that’ “the ‘other’” <code>foo "bar"</code>
        """
        result = convert_quotes(start)
        assert result == expected

    def test_clean_footnotes_asciidoc(self):
        """
        Test that we are properly removing brackets
        """
        start = '<sup class="footnote">[<a id="_footnoteref_1" class="' + \
                'footnote" href="#_footnotedef_1" title="View footnote.">' + \
                '1</a>]</sup>'
        expected = '<sup class="footnote"><a id="_footnoteref_1" ' + \
                   'class="footnote" href="#_footnotedef_1" ' + \
                   'title="View footnote.">1</a></sup>'
        result = clean_footnotes(start)
        assert result == expected

    def test_clean_footnotes_endnotes(self):
        """
        Test that we are adding a "Notes" header before our endnote sections
        """
        start = '<div id=\"footnotes\">\n<div class=\'section-break\'>' + \
                '<p>#</p></div>\n<div class="footnotes">\n<div class=\'' + \
                'section-break\'><p>#</p>'
        expected = '<div id="footnotes">\n<h2>Notes</h2>\n<div class=' + \
                   '"footnotes">\n<h2>Notes</h2>'
        result = clean_footnotes(start)
        assert result == expected
