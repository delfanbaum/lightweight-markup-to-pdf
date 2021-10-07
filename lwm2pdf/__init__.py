import re
import sys
import os
import shutil
import subprocess
from weasyprint import HTML, CSS

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


# ---------------------------------------------------------------------
# cleanup the asciidoc
# ---------------------------------------------------------------------

# beautify function
print("Beautifying asciidoc markup...")
def beautifyText(text):
    # don't beautify verse
    if text.find("[verse]\n____") == -1:
        # make sure we can still have literals/code blocks
        #r = re.compile(r'----')
        #text = re.sub(r, r'@@@@', text)
        # em dashese
        #r = re.compile(r'--')
        #text = re.sub(r, r'&#8212;', text)
        # quotes
        r = re.compile(r'"(.*?)"')
        text = re.sub(r, r'"`\1`"', text)
        # return our literals and code blocks
        #r = re.compile(r'@@@@')
        #text = #re.sub(r, r'----', text)
        # return any role markers
        r = re.compile(r'\[role\=\"\`(.*?)\`\"\]')
        text = re.sub(r, r'[role="\1"]', text)
    return text

# check for includes and if so, manage them
def checkIncludes(fn, parentPath=''):
    # get file
    dirs = fn.split("/")
    fnpath = "/".join(dirs[:-1]) + "/"
    parentText = open(fn, 'r').read()

    # check for includes
    p = re.compile(r'include\:\:(.*?).adoc')
    result = p.findall(parentText)
    if len(result) > 0:
        for x in range(len(result)):
            # get relevant information
            childFn = result[x] + ".adoc"
            # check if the child is inside a directory
            childPath = ''
            if len(childFn.split('/')) > 1:
                childPath = "/".join(childFn.split('/')[:-1])
                if os.path.isdir(targetdir + childPath) == False:
                    os.mkdir(targetdir + childPath)
            childFnPath = fnpath + childFn
            childText = open(childFnPath, 'r').read()
            # build the output file to the buildsrc directory
            open(targetdir + parentPath + childFn, 'w').write(beautifyText(childText))
            # check for includes inside in the child include
            checkIncludes(childFnPath, childPath + '/')
    # return corrected text
    return beautifyText(parentText)

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

# split the author info
print("Splitting author name for page numbering...")
def split_author_names(match):
    name = match.group(1).split(' ')
    # edge case
    if len(name) > 2:
        first = name[0]
        middle = name[1] # tbh this won't handle things well
        last = name[-1]
    else:
        first = name[0]
        last = name[-1]
    return f"<span id='authorFirstName'>{first}</span>&nbsp<span id='authorLastName'>{last}</span>"

au_r = re.compile(r'<span id="author" class="author">(.*?)</span><br>')
html = re.sub(au_r, split_author_names, html)

# if quotes, fix citation style
print("Cleaning up blockquotes...")
def swap_br_for_comma(match):
    str = match.group(1)
    newstr = f'''
        <div class="attribution">
        &#8212; {str},
    '''
    return newstr

quote_r = re.compile(r'<div class="attribution">\n&#8212; (.*?)<br>')
html = re.sub(quote_r, swap_br_for_comma, html)

# expand links (but not cross references)
print("Expanding links and fixing xrefs for print...")
def expand_links(match):
    if not match.group(1).find("#") > -1:
        expanded_link = f'{match.group(2)} (<a href="{match.group(1)}">{match.group(1)}</a>)'
        return expanded_link
    elif not match.group(0).find("class=\"footnote") > -1:
        xref = f'<a href="{match.group(1)}" data-type="xref">{match.group(2)}</a>'
        return xref
    else:
        return match.group(0)

link_r = re.compile(r'<a href="(.*?)">(.*?)</a>')
html = re.sub(link_r, expand_links, html)

# fix footnotes
print("Fixing footnotes for print...")
def fix_footnotes(match):
    # <sup class="footnote">[<a id="_footnoteref_1" class="footnote" href="#_footnotedef_1" title="View footnote.">1</a>]</sup>
    return f'<sup class="footnote">{match.group(1)}</sup>'

footnote_r = re.compile(r'<sup class="footnote">\[(.*?)\]</sup>')
html = re.sub(footnote_r, fix_footnotes, html)

# just swap hrs for breaks (will help with copy-paste to word)
html = html.replace("<hr>","<div class='section-break'><p>~</p></div>")
    
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
