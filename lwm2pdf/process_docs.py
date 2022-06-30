import subprocess
import re
import markdown2  # type: ignore


def asciidoc_to_html(fn):
    """ takes an asciidoc-formatted file and returns html """
    print("Running our input through asciidoc conversion....")
    print("Checking for asciidoctor...")
    try:
        test_asciidoctor = subprocess.run(['asciidoctor', '-v'],
                                          capture_output=True,
                                          text=True)
        if test_asciidoctor.stderr == '':
            print("Asciidoctor is present; converting with asciidoctor...")
            # make a temp preformatted file
            result = subprocess.run(['asciidoctor', '-a', "stylesheet!",
                                     "-o", "-", fn],
                                    capture_output=True,
                                    text=True)

            if result.stderr == '':
                return result.stdout

            else:
                print(f'\nError: {result.stderr}')
                print("Exiting...")
                exit()

    except FileNotFoundError:
        print("\n---\nWARNING: Asciidoctor was not found on your PATH.")
        print("\nWe will proceed with the asciidoc-py converter,")
        print("but we recommend installing asciidoctor for")
        print("best results. Some features may not be available.")
        print("See https://asciidoctor.org/ for more information.\n---")
        print("\nProceeding with asciidoc-py...")

        result = subprocess.run(['asciidoc', '-b', 'html5', '-a', 'linkcss',
                                 '-a', 'disable-javascript', "-o", "-", fn],
                                capture_output=True,
                                text=True)
        if result.returncode == 0:
            html = result.stdout
            # remove linked stylesheet....
            html = html.replace('<link rel="stylesheet" href="./asciidoc.css" type="text/css">', '')
            return html

        else:
            print()
            print(f'Error code {result.returncode}: {result.stderr}')
            exit()


def md_to_html(fn):
    """ takes a markdown file and returns html """

    print("Running input through markdown conversion....")
    text = open(fn, 'r').read()
    html = markdown2.markdown(text, extras=["fenced-code-blocks",
                                            "header-ids",
                                            "footnotes",
                                            "smarty-pants"  # to save a step
                                            ])
    return html


def markup_to_html(fn, supported_file_types):
    # handle asciidoc
    if fn.find('.adoc') > -1 or fn.find('.asciidoc') > 1:
        html = asciidoc_to_html(fn)
    
    # handle markdown
    elif fn.find('.md') > -1:
        html = md_to_html(fn)
    
    else:
        html = None
        SystemExit("Error: It appears you're trying to convert an " +
                   "unsupported file format. This script accepts only " +
                   f"{supported_file_types} files.")
    return html
