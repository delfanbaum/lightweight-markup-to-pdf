import os
import subprocess
from markdown import markdown

# ---------------------------------------------------------------------
# Asciidoctor step
# ---------------------------------------------------------------------

def asciidoc_to_html(fn):
    print("Running our input through asciidoctor....")
    result = subprocess.run(['asciidoctor', '-a', "stylesheet!", fn, "-o", "-"], capture_output=True, text=True)
    if result.stderr == '':    
        return result.stdout
    else:
        raise SystemExit(f'Error: {restult.stderr}')

def md_to_html(fn):
    print("Running input through markdown conversion....")
    with open(fn, 'r') as f:
        text = f.read()
        html = markdown(text)
    return html
