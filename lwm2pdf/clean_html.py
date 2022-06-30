import re


def clean_html(html: str, section_break_marker: str = '#') -> str:
    """
    A clean function to make the html nicer for weasyprinting
    """
    # split the author info
    au_r = re.compile(r'<span id="author" class="author">(.*?)</span><br>')
    html = re.sub(au_r, split_author_names, html)

    # just swap hrs for breaks (will help with copy-paste to word)
    html = html.replace("<hr>",
            f"<div class=\"section-break\"><p>{section_break_marker}</p></div>")
    html = html.replace("<hr />",  # markdown converted handle
            f"<div class=\"section-break\"><p>{section_break_marker}</p></div>")

    # if quotes, fix citation style
    print("Cleaning up blockquotes...")
    quote_r = re.compile(r'<div class="attribution">\n&#8212; (.*?)<br>')
    html = re.sub(quote_r, swap_br_for_comma, html)

    # expand links (and handle cross references)
    # NOTE: This does not super handle classes on xref a tags...
    print("Expanding links and fixing xrefs for print...")
    link_r = re.compile(r'<a href="(.*?)">(.*?)</a>')
    html = re.sub(link_r, expand_links_and_xrefs, html)

    # fix missing xrefs
    xrefs = re.compile(r'<a href="(.*?)" data-type="xref">(.*?)</a>')
    missing_xref_string = '<a href="#" class="missing-xref">???</a>'
    for m in re.finditer(xrefs, html):
        # if the id doesn't exist
        id = m.group(1)[1:]
        if html.find(f'id="{id}') == -1:
            print(f'\nWARNING: Missing xref to #{id}\n')
            html = html.replace(m.group(0), missing_xref_string)

    # do footnotes
    print("Fixing footnotes for print...")
    html = clean_footnotes(html)

    return html


def clean_footnotes(html):
    """ clean up footnotes """
    footnote_r = re.compile(r'<sup class="footnote">\[(.*?)\]</sup>')
    html = re.sub(footnote_r, fix_footnotes, html)

    # asciidoc
    endnotes_r = "<div id=\"footnotes\">\n<div class='section-break'><p>#</p></div>"
    html = html.replace(endnotes_r, 
                        '<div id="footnotes">\n<h2>Notes</h2>')
    # markdown
    endnotes_r_md = '<div class="footnotes">\n<div class=\'section-break\'><p>#</p>'
    html = html.replace(endnotes_r_md, 
                        '<div class="footnotes">\n<h2>Notes</h2>')
    return html


# Match functions
def split_author_names(match):
    """ if possible, split author name """
    name = match.group(1).split(' ')
    # edge case
    if len(name) > 2:
        first = name[0]
        last = name[-1]
    else:
        first = name[0]
        last = name[-1]
    return f"<span id='authorFirstName'>{first}</span>&nbsp;" + \
           f"<span id='authorLastName'>{last}</span>"


def swap_br_for_comma(match):
    """ fix for asciidoc(tor) attributions """
    str = match.group(1)
    newstr = f'<div class="attribution">&#8212; {str}, '
    return newstr


def expand_links_and_xrefs(match):
    """
    since this is print, expand links such that they appear after anchored text
    """
    if not match.group(1).find("#") > -1:
        expanded_link = f'{match.group(2)} (<a href="{match.group(1)}">{match.group(1)}</a>)'
        return expanded_link

    # do xrefs but not footnotes... assuming all non-footnotes are xrefs
    elif (
        match.group(0).find("class=\"footnote") == -1 and
        match.group(0).find("href=\"#fn-") == -1 and
        match.group(0).find("href=\"#_footnoteref_") == -1
       ):
        xref = f'<a href="{match.group(1)}" data-type="xref">{match.group(2)}</a>'
        return xref
    else:
        return match.group(0)


def fix_footnotes(match):
    """
    Takes the <sup> footnotes and renders them more appropriately.
    """
    return f'<sup class="footnote">{match.group(1)}</sup>'
