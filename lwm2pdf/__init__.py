import re
import sys
import os
import shutil
import subprocess
from weasyprint import HTML, CSS
from cleanhtml import clean_html
from processadoc import check_includes

print("\n==============================================================")
print("Starting the PDF builder script for lighweight markup files...")
print("================================================================\n")

# get file
print("Checking for our input file...")
if len(sys.argv) > 1:
    fn = sys.argv[1]
else:
    fn = input('\nPlease enter the relative path of the \ndocument you\'d like to build: ')

# get just the filename sans ".asciidoc/adoc"
adoc_fn = fn.split("/")[-1].split('.')[0]

# place where we put our build files
build_file = os.path.dirname(__file__)
build_home = str(os.path.abspath(build_file))

parentdir = build_home + '/output/'
targetdir = build_home + '/output/src/'
sass = build_home + '/styles/manuscript.scss'
css = build_home + '/styles/manuscript.css'

# output file name
output_html = build_home + '/output/src/buildfile.html'
output_fn = build_home + f'/output/{adoc_fn}.pdf'
toc_check_html = build_home + '/output/src/pre_toc_buildfile.html'
toc_check_fn = build_home + f'/output/pre_toc_{adoc_fn}.pdf'

# build toc?
build_toc = True

# make sure our buildsrc directory exists and is clean
print("Clean up output directory...")
if os.path.isdir(parentdir):
    shutil.rmtree(parentdir)
os.mkdir(parentdir)
# there is a better way to do this I'm sure, but...
os.mkdir(targetdir)

# check includes
text = checkIncludes(fn)
# make our buildfile
buildfile = targetdir + 'buildfile.adoc'
open(buildfile, 'w').write(text)

# ---------------------------------------------------------------------
# Asciidoctor step
# ---------------------------------------------------------------------

# run it through asciidoc
print("Running our input through asciidoctor....")
try:
  run_adoctor = f"asciidoctor -a stylesheet! {buildfile} -D {targetdir} -o buildfile.html"
  if os.system(run_adoctor) != 0:
      raise Exception('Error: there was a problem running asciidoctor. Please ensure you have asciidoctor installed on your path.')
except:
  print("Error: something went wrong while running asciidoctor; please check your configuration.")

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

print("Cleaning up html asciidoctor output...")
html = open(output_html, 'r').read()

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

print("Building PDF...")

# Build final PDF
try:
    HTML(output_html).write_pdf(
        output_fn,
        stylesheets=[CSS(string=styles)])
    print(f"\nSuccess! A PDF from {adoc_fn}.adoc has been successfully built and saved to:\n{output_fn}\n")
except:
    print("There was an error building the PDF. Please ensure you've\ninstalled all requisite dependencies.")

# Let the user know where it lives now


openPDF = input('Do you want to open the PDF? [y/n] ')
if openPDF == 'y':
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
