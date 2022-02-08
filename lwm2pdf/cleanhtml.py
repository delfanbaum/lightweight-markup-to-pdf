import re

# Clean function to make html nicer for weasyprinting
def clean_html(html: str, section_break_marker: str = '#') -> str:
    # split the author info
    print("Splitting author name for page numbering...")
    au_r = re.compile(r'<span id="author" class="author">(.*?)</span><br>')
    html = re.sub(au_r, split_author_names, html)

    # just swap hrs for breaks (will help with copy-paste to word)
    html = html.replace("<hr>",
            f"<div class=\"section-break\"><p>{section_break_marker}</p></div>")
    html = html.replace("<hr />", # markdown converted handle
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
    missing_xref_string = f'<a href="#" class="missing-xref">???</a>'
    for m in re.finditer(xrefs, html):
        # if the id doesn't exist
        id = m.group(1)[1:]
        if html.find(f'id="{id}') == -1:
            print(f'\nWARNING: Missing xref to #{id}\n')
            html = html.replace(m.group(0), missing_xref_string)

    # do footnotes 
    print("Fixing footnotes for print...")
    html = clean_footnotes(html)

    # make pretty quotes
    try:
        print("Making quotes look nice for print...")
        html = convert_quotes(html)
    except:
        print("Error converting quotes... continuing.")

    return html

# Convert quotes
def convert_quotes(html):
    in_codeblock = False
    in_verse = False

    # don't match attrs or preformatted quotes (asciidoc)
    double_quote_strings = re.compile(r'(?<!=)"(.*?)"')
    single_quote_strings = re.compile(r"'(.*?)'")
    code_strings = re.compile(r'<code(.*?)>(.*?)</code>')

    # language-specific things
    split_html = html.split('\n')
    for ln_no, line in enumerate(split_html):
        if line.find('<pre') > -1 and line.find('</pre>') == -1:
            in_codeblock = True
        # semi-edge case, but
        if line.find('class="verseblock') > -1:
            in_verse = True
        # Only swap quotes if we're in a code block
        if not in_codeblock == True or in_verse == True:
            #if the line has a tag in it, separate out the tagss
            if line.find('>') > -1: 
                line = line.replace('>',">\n")
            # do the conversions
            line = re.sub(double_quote_strings, curly_double_quote_pairs, line)
            line = re.sub(single_quote_strings, curly_single_quote_pairs, line)
            # replace it before workign on code
            line = line.replace('\n', '')
            line = re.sub(code_strings, fix_code_tags, line)
            split_html[ln_no] = line
        # if after (not) processing our line, we find that it terminates a 
        # code block, toggle in_codeblock
        if line.find('</pre>') > -1:
            in_codeblock = False
            in_verse = False
    return ('\n').join(split_html)


def clean_footnotes(html):
    # fix footnotes
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
    name = match.group(1).split(' ')
    # edge case
    if len(name) > 2:
        first = name[0]
        #middle = name[1] # tbh this won't handle things well
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

def expand_links_and_xrefs(match):
    if not match.group(1).find("#") > -1:
        expanded_link = f'{match.group(2)} (<a href="{match.group(1)}">{match.group(1)}</a>)'
        return expanded_link
    # do xrefs but not footnotes... assuming all non-footnotes are xrefs   
    elif match.group(0).find("class=\"footnote") == -1 and match.group(0).find("href=\"#fn-") == -1 and match.group(0).find("href=\"#_footnoteref_") == -1:
        xref = f'<a href="{match.group(1)}" data-type="xref">{match.group(2)}</a>'
        return xref
    else:
        return match.group(0)

def fix_footnotes(match):
    # <sup class="footnote">[<a id="_footnoteref_1" class="footnote" href="#_footnotedef_1" title="View footnote.">1</a>]</sup>
    return f'<sup class="footnote">{match.group(1)}</sup>'

def curly_double_quote_pairs(match):
    # handle case of href="some[" attr="]some other"
    try:
        if match.group(1).find('=') == -1 and \
            match.group(1).find('<') == -1 and \
            match.group(1).find('>') == -1 and \
            match.group(1)[0] != "`":
            return f'“{match.group(1)}”'
        else: 
            return match.group(0)
    except:
        print(f'Something went wrong at {match.group(0)}')
        return match.group(0)

def curly_single_quote_pairs(match):
    try:
        if match.group(1).find('=') == -1 and \
            match.group(1).find('<') == -1 and \
            match.group(1).find('>') == -1 and \
            match.group(1)[0] != "`":
            return f'‘{match.group(1)}’'
        else: 
            return match.group(0)
    except:
        print(f'Something went wrong at {match.group(0)}')
        return match.group(0)

def fix_code_tags(match):
    double_quotes = re.compile(r'“|”')
    single_quotes = re.compile(r'‘|’')
    code = re.sub(double_quotes, '"', match.group(2))
    code = re.sub(single_quotes, "'", code)
    return f'<code{match.group(1)}>{code}</code>'

