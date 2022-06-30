from lwm2pdf.postprocess_docs import postprocess_html_quotes


def test_basic_dbl_quote():
    """ happy path test case for double quotes """
    start = '<p>Some "quoted text"</p>'
    result = postprocess_html_quotes(start)
    expected = '<p>Some “quoted text”</p>'
    assert result == expected


def test_basic_sgl_quote():
    """ happy path test case for single quotes """
    start = "<p>Some 'quoted text'</p>"
    result = postprocess_html_quotes(start)
    expected = '<p>Some ‘quoted text’</p>'
    assert result == expected


def test_inside_quote_us():
    """ happy path test case for single quotes inside double """
    start = "<p>Some \"'quoted text'\"</p>"
    result = postprocess_html_quotes(start)
    expected = '<p>Some “‘quoted text’”</p>'
    assert result == expected


def test_inner_elements_simple():
    """ test for elements inside a quote thing """
    start = """
            <p>Some "quoted <em>emphasized</em> text"</p>
            <p>Some 'single <strong>stuff</strong>'</p>
            """
    result = postprocess_html_quotes(start)
    expected = """
<p>Some “quoted <em>emphasized</em> text”</p>
<p>Some ‘single <strong>stuff</strong>’</p>
"""
    assert result == expected


def test_inner_elements_more_complex():
    """ test for elements inside a quote thing in a harder context"""
    start = """<p>Some "quoted <em>emphasized</em> text"
Some 'single <strong>stuff</strong>'</p>
"""
    result = postprocess_html_quotes(start)
    expected = """<p>Some “quoted <em>emphasized</em> text”
Some ‘single <strong>stuff</strong>’</p>
"""
    assert result == expected


def test_dont_smart_quote_code():
    """ ensure we're not screwing with code """
    start = '<p>Some <code>"String"</code></p>'
    result = postprocess_html_quotes(start)
    expected = '<p>Some <code>"String"</code></p>'
    assert result == expected


def test_dont_smart_quote_pre():
    """ ensure we're not screwing with code """
    start = '<p>Some <pre>"String"</pre></p>'
    result = postprocess_html_quotes(start)
    expected = '<p>Some <pre>"String"</pre></p>'
    assert result == expected
