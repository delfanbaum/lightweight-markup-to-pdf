import os, subprocess, re
import markdown2 # type: ignore

# ---------------------------------------------------------------------
# Asciidoctor step
# ---------------------------------------------------------------------

def asciidoc_to_html(fn):
    print("Running our input through asciidoc conversion....")
    print("Checking for asciidoctor...")
    text = pre_convert_quotes(fn)
    try: 
        test_asciidoctor = subprocess.run(['asciidoctor', '-v'], 
                            capture_output=True, text=True)
        if test_asciidoctor.stderr == '':
            print("Asciidoctor is present; convering with asciidoctor...") 
            result = subprocess.run(['asciidoctor', '-a', "stylesheet!", 
            "-o","-",
            fn], 
            # input=text, 
            capture_output=True, text=True)
        if result.stderr == '':    
            return result.stdout
        else:
            # raise SystemExit(f'Error: {result.stderr}')
            print(f'Error: {result.stderr}')

    except FileNotFoundError:
        print("\n---\nWARNING: Asciidoctor was not found on your PATH.")
        print("\nWe will proceed with the asciidoc-py converter,")
        print("but we recommend installing asciidoctor for")
        print("best results. Some features may not be available.")
        print("See https://asciidoctor.org/ for more information.\n---")
        print("\nProceeding with asciidoc-py...")
        result = subprocess.run(['asciidoc', '-b', 'html5', '-a', 'linkcss',
                                    '-a', 'disable-javascript', '-'],
                                    input=text, capture_output=True, text=True)
        if result.returncode == 0:    
            html =  result.stdout
            # remove linked stylesheet....
            html = html.replace('<link rel="stylesheet" href="./asciidoc.css" type="text/css">', '')
            return html
        else:
            print()
            # raise SystemExit(f'Error: {result.stderr}')
            print(f'Error code {result.returncode}: {result.stderr}')                             
            exit()

def md_to_html(fn):
    print("Running input through markdown conversion....")
    text = pre_convert_quotes(fn)
    html = markdown2.markdown(text, extras=["fenced-code-blocks",
                                            "header-ids",
                                            "footnotes",
                                            "smarty-pants" # save a step?
                                            ])
    return html

def pre_convert_quotes(fn):
    in_codeblock = False
    # don't match attrs or preformatted quotes (asciidoc)
    double_quote_strings = re.compile(r'(?<!=)"[^`](.*?)"')
    single_quote_strings = re.compile(r" '[^`](.*?)' ")
    # language-specific things
    if fn.find("adoc") > -1 or fn.find("asciidoc") > -1:
        codeblock_fence = '----'
        codeblock_space = '  '
    elif fn.find(".md") > -1:
        codeblock_fence = '```'
        codeblock_space = '    '
        # quote marker (don't match preformated)
        # file info
    else:
        print("We do not yet support smartquote conversion for this filetype.")
        print("Passing plain text to coverter...")
        text = open(fn, 'r').read()
        return text
    # now do the conversion
    file = open(fn, 'r')
    lines = file.readlines()
    for line in lines:
        if line == codeblock_fence:
            in_codeblock = not in_codeblock
        if not in_codeblock == True and line[0:len(codeblock_space) - 1] != codeblock_space: 
            # i.e., you are not in a codeblock
            line = re.sub(double_quote_strings, curly_double_quote_pairs, line)
            line = re.sub(single_quote_strings, curly_single_quote_pairs, line)
    return ('').join(lines)

def curly_double_quote_pairs(match):
    # handle case of href="some[" attr="]some other"
    if match.group(1).find('=') == -1:
        return f'“{match.group(1)}”'
    else: 
        return match.group(0)

def curly_single_quote_pairs(match):
    if match.group(1).find('=') == -1:
        return f' ‘{match.group(1)}’ '
    else: 
        return match.group(0)
