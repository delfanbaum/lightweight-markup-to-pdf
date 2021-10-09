#!/usr/bin/python3
import sys
import os
import shutil
import subprocess
from options import get_lwm2pdf_options
from os.path import abspath
from processdocs import asciidoc_to_html, md_to_html
from cleanhtml import clean_html
from weasyprint import HTML, CSS

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
    output_fn = os.getcwd() + f'/{options.output_dir}/{fn_name_only}.pdf'
else:
    print("Using default output destination...")
    output_fn = os.getcwd()+ f'/{fn_name_only}.pdf' 

# get stylesheet information
if options.stylesheet:
    css = abspath(options.stylesheet)
else:  # defaults
    script_dir = os.path.dirname(__file__)
    script_home = str(os.path.abspath(script_dir))
    styles_home = ('/').join(script_home.split('/')[0:-1])
    css = styles_home + '/styles/manuscript.css'



print("\n==============================================================")
print("Starting the PDF builder script for lighweight markup files...")
print("================================================================\n")

# get file
# TO DO: parse based on current dir, add checking, etc.

buildfiles_dir = os.getcwd() + f'/{fn_name_only}-src'
output_html = f'{buildfiles_dir}/buildfile.html'


# make sure our buildsrc directory exists and is clean
print("Creating buildfiles directory...")
# there is a better way to do this I'm sure but this works for now
if os.path.isdir(buildfiles_dir):
    shutil.rmtree(buildfiles_dir)
os.mkdir(buildfiles_dir)

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
        try: # assume first that we're on a mac, as we usually are
            os.system(f"open {output_fn}")
        except:
            
            try: # well maybe we're working on a linux machine
                os.system(f'xdg-open {output_fn}')
            except OSError as error_not_linux:
                try: # windows? 
                    os.startfile(output_fn)
                except OSError as error_not_win:
                    # Something went wrong here, so let's show the user what 
                    # happened.
                    print("Sorry, I can't seem to open the file. Try opening with your file browser.")
                    print("Error log:")
                    # print(error_not_mac)
                    print(error_not_linux)
                    print(error_not_win)


print("Building PDF...")

# Build final PDF
success = False

try:
    HTML(output_html).write_pdf(
        output_fn,
        stylesheets=[CSS(string=styles)])
    # Let the user know where it lives now
    print(f"\nSuccess! A PDF from {fn} has been successfully built and saved to:\n{output_fn}\n")
    success = True
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



if success == True:
    open_pdf()