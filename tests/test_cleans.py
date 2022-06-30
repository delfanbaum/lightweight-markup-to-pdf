from lwm2pdf.clean_html import clean_footnotes, clean_html


class TestCleans:
    """
    Component tests for clean_html()
    """

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

    def test_clean_split_authors(self):
        """ tests author split names """
        start = '<span id="author" class="author">John Smith</span><br>'
        expected = "<span id='authorFirstName'>John</span>&nbsp;" + \
                   "<span id='authorLastName'>Smith</span>"
        
        assert clean_html(start) == expected

    def test_blockquotes(self):
        start = '<div class="attribution">\n&#8212;' + \
                ' Jane Smith<br>"Some Text"</div>'
        expected = '<div class="attribution">&#8212;' + \
                   ' Jane Smith, "Some Text"</div>'
        assert clean_html(start) == expected

    def test_links(self):
        start = '<a href="http://example.com">text</a>'
        expect = 'text (<a href="http://example.com">http://example.com</a>)'
        assert clean_html(start) == expect

    def test_existing_xrefs(self):
        start = '<a id="some_mark">anchor text"</a> ' + \
                '<a href="#some_mark">text</a>'
        expect = '<a id="some_mark">anchor text"</a> ' + \
                 '<a href="#some_mark" data-type="xref">text</a>'
        assert clean_html(start) == expect

    def test_missing_xrefs(self):
        start = '<a href="#some_mark">text</a>'
        expect = '<a href="#" class="missing-xref">???</a>'
        assert clean_html(start) == expect
