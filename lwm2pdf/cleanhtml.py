import re

# Clean function

# takes a string
def clean_html(html: str, section_break_marker: str = '#') -> str:
    # split the author info
    print("Splitting author name for page numbering...")
    au_r = re.compile(r'<span id="author" class="author">(.*?)</span><br>')
    html = re.sub(au_r, split_author_names, html)

    # if quotes, fix citation style
    print("Cleaning up blockquotes...")
    quote_r = re.compile(r'<div class="attribution">\n&#8212; (.*?)<br>')
    html = re.sub(quote_r, swap_br_for_comma, html)

    # expand links (but not cross references)
    print("Expanding links and fixing xrefs for print...")
    link_r = re.compile(r'<a href="(.*?)">(.*?)</a>')
    html = re.sub(link_r, expand_links, html)

    # fix footnotes
    print("Fixing footnotes for print...")
    footnote_r = re.compile(r'<sup class="footnote">\[(.*?)\]</sup>')
    html = re.sub(footnote_r, fix_footnotes, html)

    # just swap hrs for breaks (will help with copy-paste to word)
    html = html.replace("<hr>",
            f"<div class='section-break'><p>{section_break_marker}</p></div>")

    return html


# Match functions
def split_author_names(match):
    name = match.group(1).split(' ')
    # edge case
    if len(name) > 2:
        first = name[0]
        middle = name[1] # tbh this won't handle things well
        last = name[-1]
    else:
        first = name[0]
        last = name[-1]
    return f"<span id='authorFirstName'>{first}</span>&nbsp<span id='authorLastName'>{last}</span>"

def swap_br_for_comma(match):
    str = match.group(1)
    newstr = f'''
        <div class="attribution">
        &#8212; {str},
    '''
    return newstr

def expand_links(match):
    if not match.group(1).find("#") > -1:
        expanded_link = f'{match.group(2)} (<a href="{match.group(1)}">{match.group(1)}</a>)'
        return expanded_link
    elif not match.group(0).find("class=\"footnote") > -1:
        xref = f'<a href="{match.group(1)}" data-type="xref">{match.group(2)}</a>'
        return xref
    else:
        return match.group(0)

def fix_footnotes(match):
    # <sup class="footnote">[<a id="_footnoteref_1" class="footnote" href="#_footnotedef_1" title="View footnote.">1</a>]</sup>
    return f'<sup class="footnote">{match.group(1)}</sup>'
