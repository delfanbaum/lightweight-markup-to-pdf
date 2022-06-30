import bs4
import re

non_quoted_elements = ["code", "pre"]


def add_smart_quotes_pairs(string):
    """ add paired quotes """
    r = re.compile(r"'(.*?)'")
    s_quoted_str = re.sub(r, r'‘\1’', string)
    r = re.compile(r'"(.*?)"')
    quoted_str = re.sub(r, r'“\1”', s_quoted_str)
    return quoted_str


def add_double_quotes_to_children(parent):
    """ recursively add quotes to child strings """
    unpaired = False
    for child in parent.children:
        if child.name not in non_quoted_elements:
            if child.string:
                quoted_str = add_smart_quotes_pairs(child.string)
                # handle quotes around children
                if (
                    quoted_str == child.string and
                    child.string.find('"') > -1
                ):
                    if not unpaired:
                        quoted_str = child.string.replace('"', '“')
                        unpaired = True
                    elif unpaired:
                        quoted_str = child.string.replace('"', '”')
                        unpaired = False

                child.string.replace_with(quoted_str)
            else:
                add_double_quotes_to_children(child)


def add_single_quotes_to_children(parent):
    """ recursively add quotes to child strings """
    unpaired = False
    for child in parent.children:
        if child.name not in non_quoted_elements:
            if child.string:
                quoted_str = add_smart_quotes_pairs(child.string)
                # handle quotes around children
                if (
                    quoted_str == child.string and
                    child.string.find("'") > -1
                ):
                    if not unpaired:
                        quoted_str = child.string.replace("'", "‘")
                        unpaired = True
                    elif unpaired:
                        quoted_str = child.string.replace("'", "’")
                        unpaired = False

                child.string.replace_with(quoted_str)
            else:
                add_single_quotes_to_children(child)


def postprocess_html_quotes(html):
    """ add smart double quotes """
    soup = bs4.BeautifulSoup(html, "html.parser")
    paras = soup.find_all('p')
    for p in paras:
        p_str = p.string
        if p.string:  # no inner elements
            quoted_str = add_smart_quotes_pairs(p_str)
            p_str.replace_with(quoted_str)
        else:
            add_double_quotes_to_children(p)
            add_single_quotes_to_children(p)
    return str(soup)
