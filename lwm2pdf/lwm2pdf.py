#!/usr/bin/python3
import sys
import os
import shutil
import subprocess
import argparse
from weasyprint import HTML, CSS
from cleanhtml import clean_html
from processdocs import asciidoc_to_html, md_to_html

# for help and also bookkeepting
supperted_file_types = '*.adoc, *.asciidoc, or *.md'



# options parsing

cli_options_parser = argparse.ArgumentParser(prog='lwm2pdf',
                     usage='%(prog)s [options]',
                     description=f'Converts {supperted_file_types} into PDFs based on default or user stylesheet (css).')

cli_options_parser.add_argument('-i', '--input', 
                                dest='input',
                                action='store',
                                nargs=1, 
                                type=str, 
                                required=True,
                                help=f'the file to convert ({supperted_file_types})')

cli_options_parser.add_argument('-o', '--output',
                                dest='output',
                                nargs=1,
                                type=str,
                                required=False,
                                help='output filename and destination (optional)')

cli_options_parser.add_argument('-s', '--stylesheet',
                                dest='stylesheet',
                                nargs=1,
                                type=str,
                                required=False,
                                help='select user stylesheet (css) (optional)')
cli_options_parser.add_argument('-p', '--preserve-buildfiles',
                                dest='save_buildfile',
                                required=False,
                                help='preserve buildfiles in output/src in current working directory')


options = cli_options_parser.parse_args()

# configuration
print("\n==============================================================")
print("Starting the PDF builder script for lighweight markup files...")
print("================================================================\n")

# get file
# TO DO: parse based on current dir, add checking, etc.
fn = options.input

# get just the filename sans ".asciidoc/adoc"
split_fn = fn.split("/")[-1].split('.')[0]

# place where we put our build files
current_working_dir = os.getcwd() 
script_dir = os.path.dirname(__file__)
script_home = str(os.path.abspath(script_dir))
styles_home = ('/').join(script_home.split('/')[0:-1])

parent_dir = current_working_dir + '/output/'
target_dir = current_working_dir + '/output/src/'

sass = styles_home + '/styles/manuscript.scss'
css = styles_home + '/styles/manuscript.css'

# output file name
output_html = target_dir + 'buildfile.html'
print(output_html)
output_fn = parent_dir + f'{split_fn}.pdf'


# make sure our buildsrc directory exists and is clean
print("Create or cleanup output directory...")
# there is a better way to do this I'm sure but this works for now
if os.path.isdir(parent_dir):
    shutil.rmtree(parent_dir)
os.mkdir(parent_dir)
os.mkdir(target_dir)

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
    SystemExit("Error: It appears you're trying to convert a nonsupported file format.")


# ---------------------------------------------------------------------
# Generate CSS if needed
# ---------------------------------------------------------------------

# add the css...
# get most up-to-date stylesheet
try:
    print("Checking to see if sass is installed...")
    subprocess.run(['sass', '-v'], check = True)
    print("Creating up-to-date stylesheet(s)...")
    if not os.path.exists(css) == True:
        os.system(f"sass --style=compressed {sass} {css}")
    if not os.path.getmtime(css) >= os.path.getmtime(sass):
        os.system(f"sass --style=compressed {sass} {css}")
    styles = open(css, 'r').read()
except subprocess.CalledProcessError:
    print ("You don't have sass installed on your path. Using the existing stylesheet...")

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
print(f"Writing styled output for Word copy/paste to buildfile_styled...")
html_with_styles = html.replace('</head>', f'<style>{styles}</style></head>')

open(output_html.replace('.html', "_styled.html"), 'w').write(html_with_styles)

# ---------------------------------------------------------------------
# Build the (final) PDF
# ---------------------------------------------------------------------

# helper 
def open_pdf():
    ask_to_open = input('Do you want to open the PDF? [y/n] ')
    if ask_to_open == 'y':
        try: # assume first that we're on a mac, as we usually are
            os.system(f"open {output_fn}")
        except OSError as error_not_mac:
            print("")
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
                    print(error_not_mac)
                    print(error_not_linux)
                    print(error_not_win)


print("Building PDF...")

# Build final PDF
try:
    HTML(output_html).write_pdf(
        output_fn,
        stylesheets=[CSS(string=styles)])
    # Let the user know where it lives now
    print(f"\nSuccess! A PDF from {fn} has been successfully built and saved to:\n{output_fn}\n")
    open_pdf()
except:
    print("There was an error building the PDF. Please ensure you've\ninstalled all requisite dependencies.")


