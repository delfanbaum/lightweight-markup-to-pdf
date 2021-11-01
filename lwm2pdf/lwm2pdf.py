#!/usr/bin/python3
import os, subprocess
import shutil
from options import get_lwm2pdf_options
from os.path import abspath
from processdocs import asciidoc_to_html, md_to_html
from cleanhtml import clean_html
from weasyprint import HTML, CSS # type: ignore
from weasyprint.fonts import FontConfiguration # type: ignore


supperted_file_types = '*.adoc, *.asciidoc, or *.md'

# for later things


#================================================
# Options
#================================================

# get options
options = get_lwm2pdf_options(supperted_file_types)

# get our input file information
fn = options.input
fn_full_path = abspath(fn)
fn_name_only = fn.split("/")[-1].split('.')[0]

# get output destination
if options.output:
    if not options.output[-4:] == '.pdf':
        print('Error: Your output filetype must be ".pdf"')
        exit()
    else:
        output_fn = abspath(options.output)
        print(output_fn)
elif options.output_dir:
    if options.output_dir[-1] == '/':
        output_fn = os.getcwd() + f'/{options.output_dir}{fn_name_only}.pdf'
    else:    
        output_fn = os.getcwd() + f'/{options.output_dir}/{fn_name_only}.pdf'
else:
    print("Using default output destination...")
    output_fn = os.getcwd()+ f'/{fn_name_only}.pdf' 

# get stylesheet information
if options.stylesheet:
    css = abspath(options.stylesheet)
else:  # defaults
    print("Using default stylesheet...")
    script_dir = os.path.dirname(__file__)
    script_home = str(os.path.abspath(script_dir))
    styles_home = ('/').join(script_home.split('/')[0:-1])
    css = styles_home + '/themes/manuscript.css'

print("\n==============================================================")
print("Starting the PDF builder script for lighweight markup files...")
print("================================================================\n")

print("Creating buildfiles directory...")

if options.buildfile_dir:
    buildfiles_dir = abspath(options.buildfile_dir)
else:
    buildfiles_dir = os.getcwd() + f'/{fn_name_only}-src'

if not os.path.isdir(buildfiles_dir):
    # no longer cleaning b/c it'll just overwrite anyway
    os.mkdir(buildfiles_dir)

output_html = f'{buildfiles_dir}/{fn_name_only}-buildfile.html'

# ---------------------------------------------------------------------
# Conversion step
# ---------------------------------------------------------------------

# handle asciidoc
if fn.find('.adoc') > -1 or fn.find('.asciidoc') > 1:
    html = asciidoc_to_html(fn)

# handle markdown
elif fn.find('.md') > -1:
    html = md_to_html(fn)

else:
    SystemExit(f"Error: It appears you're trying to convert a nonsupported file format. This script accepts only {supperted_file_types} files.")

# ---------------------------------------------------------------------
# Cleanup the html
# ---------------------------------------------------------------------

html = clean_html(html)
    
# ---------------------------------------------------------------------
# Create html output for building and also for troubleshooting
# ---------------------------------------------------------------------

# finish for pdf_build
open(output_html, 'w').write(html)

# create output for checking/pasting to word
styles = open(css, 'r').read()
print(f"Writing styled output for Word copy/paste to buildfile_styled...")
html_with_styles = html.replace('</head>', f'<style>{styles}</style></head>')

open(output_html.replace('.html', "_styled.html"), 'w').write(html_with_styles)

# ---------------------------------------------------------------------
# Build the (final) PDF
# ---------------------------------------------------------------------

# helper 
def open_pdf():
    # need to rewrite this with subproces?
    ask_to_open = input('Do you want to open the PDF? [y/n] ')
    if ask_to_open == 'y':
        try:
            try_mac = subprocess.run(['open', output_fn],
                                    capture_output=True, text=True)
            if try_mac.stderr == '':    
                return try_mac.stdout                                    
        except FileNotFoundError:
            try: 
                try_linux = subprocess.run(['xdg-open', output_fn],
                                    capture_output=True, text=True)
                if try_linux.stderr == '':    
                    return try_linux.stdout   
            except FileNotFoundError:
                try: 
                    try_pc = subprocess.run(['open', output_fn],
                                    capture_output=True, text=True)
                    if try_pc.stderr == '':    
                        return try_pc.stdout                   
                except:
                    print("Sorry, we can't seem to open the file. Try opening with your file browser.")

print("Building PDF...")

# Build final PDF
try:
    font_config= FontConfiguration()
    HTML(output_html).write_pdf(
        output_fn,
        stylesheets=[CSS(string=styles)],
        font_config=font_config)
    # Let the user know where it lives now
    print(f"\nSuccess! A PDF from {fn} has been successfully built and saved to:\n{output_fn}\n")
    open_pdf()
except AttributeError as ae:
    print(ae)
except Exception as unk_e:
    print(f"There was an error building the PDF.\n{Exception}\n{unk_e}")

# Cleanup build files if they're not wanted
if not options.save_buildfile and os.path.isdir(buildfiles_dir):
    shutil.rmtree(buildfiles_dir)
# elif options.output_dir:
#     subprocess to move the directory
#     mv -r buildfiles_dir
# else: # move them to wherever the output file is
