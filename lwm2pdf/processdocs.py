import subprocess
import markdown2 # type: ignore

# ---------------------------------------------------------------------
# Asciidoctor step
# ---------------------------------------------------------------------

def asciidoc_to_html(fn):
    print("Running our input through asciidoc conversion....")
    print("Checking for asciidoctor...")
    try: 
        test_asciidoctor = subprocess.run(['asciidoctor', '-v'], 
                            capture_output=True, text=True)
        if test_asciidoctor.stderr == '':
            print("Asciidoctor is present; converting with asciidoctor...") 
            result = subprocess.run(['asciidoctor', '-a', "stylesheet!", fn, "-o", "-"], capture_output=True, text=True)
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
        result = subprocess.run(['asciidoc', '-b', 'html5', '-a', 'linkcss', '-a', 'disable-javascript', '-o', '-', fn],
                                    capture_output=True, text=True)
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
    with open(fn, 'r') as f:
        text = f.read()
        html = markdown2.markdown(text, extras=["fenced-code-blocks",
                                                "header-ids",
                                                "footnotes",
                                                "smarty-pants" # save a step?
                                                ])
    return html
