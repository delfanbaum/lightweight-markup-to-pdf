#!/usr/bin/python3
import os, subprocess
import shutil
from options import get_lwm2pdf_options
from os.path import abspath
from processdocs import asciidoc_to_html, md_to_html
from cleanhtml import clean_html
from weasyprint import HTML, CSS # type: ignore
from weasyprint.fonts import FontConfiguration # type: ignore

supported_file_types = '*.adoc, *.asciidoc, or *.md'

# get output destination
def get_output_fn(options):
    """
    Takes options and returns output filename
    """
    # get the name only
    fn = options.input.split("/")[-1].split('.')[0]

    if options.output:
        if not options.output[-4:] == '.pdf':
            print('Error: Your output filetype must be ".pdf"')
            exit()
        else:
            output_fn = abspath(options.output)
            print(output_fn)
    elif options.output_dir:
        if options.output_dir[-1] == '/':
            output_fn = os.getcwd() + f'/{options.output_dir}{fn}.pdf'
        else:    
            output_fn = os.getcwd() + f'/{options.output_dir}/{fn}.pdf'
    else:
        # print("Using default output destination...")
        output_fn = os.getcwd()+ f'/{fn}.pdf' 
    return output_fn

# get stylesheet information
def get_stylesheet(options):
    """
    Takes options and returns css path
    """
    if options.stylesheet:
        css = abspath(options.stylesheet)
    else:  # defaults
        print("Using default stylesheet...")
        script_dir = os.path.dirname(__file__)
        script_home = str(os.path.abspath(script_dir))
        styles_home = ('/').join(script_home.split('/')[0:-1])
        css = styles_home + '/themes/manuscript.css'
    return css

def create_buildfiles_dir(options):
    """
    Takes options and returns buildfiles directory
    path and output_html name
    """
    # get only the name no extension
    fn = options.input.split("/")[-1].split('.')[0]

    if options.buildfile_dir:
        buildfiles_dir = abspath(options.buildfile_dir)
    else:
        buildfiles_dir = os.getcwd() + f'/{fn}-src'

    if not os.path.isdir(buildfiles_dir):
        # no longer cleaning b/c it'll just overwrite anyway
        os.mkdir(buildfiles_dir)
    output_html = f'{buildfiles_dir}/{fn}-buildfile.html'
    
    return output_html, buildfiles_dir

def convert_markup_to_html(fn, supported_file_types):
    """
    Takes a markup file and returns html
    """

    # handle asciidoc
    if fn.find('.adoc') > -1 or fn.find('.asciidoc') > 1:
        html = asciidoc_to_html(fn)

    # handle markdown
    elif fn.find('.md') > -1:
        html = md_to_html(fn)

    else:
        SystemExit(f"Error: It appears you're trying to convert a nonsupported file format. This script accepts only {supported_file_types} files.")
    return html


# Build final PDF
def build_pdf_from_html(source_fn, output_html, output_fn, styles):
    """
    takes a source name, html file, output location, and css, and creates a pdf
    """
    try:
        font_config = FontConfiguration()
        HTML(output_html).write_pdf(
            output_fn,
            stylesheets=[CSS(string=styles)],
            font_config=font_config)
        # Let the user know where it lives now
        print(f"\nSuccess! A PDF from {source_fn} has been successfully built and saved to:\n{output_fn}\n")
        open_pdf(output_fn)
    except AttributeError as ae:
        print(ae)
    except Exception as unk_e:
        print(f"There was an error building the PDF.\n{Exception}\n{unk_e}")

# helper 
def open_pdf(output_fn):
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

def main():
    # get options
    options = get_lwm2pdf_options(supported_file_types)

    # get our input file information
    fn = options.input
    fn_full_path = abspath(fn)
    fn_name_only = fn.split("/")[-1].split('.')[0]

    # get output information
    output_fn = get_output_fn(options)
    # get stylesheet
    css = get_stylesheet(options)
    with open(css, 'r') as f:
        styles = f.read()
    # create build dir, get out_fn
    output_html, buildfiles_dir = create_buildfiles_dir(options, fn_name_only)
    # convert step
    html = convert_markup_to_html(fn_full_path)
    # clean and write html
    html = clean_html(html)
    with open(output_html, 'w') as f:
        f.write(html)
    # write styles into styled saver
    with open(output_html.replace('.html', "_styled.html"), 'w') as f:
        html_with_styles = html.replace('</head>', f'<style>{styles}</style></head>')
        f.write(html_with_styles)

    # build the pdf
    build_pdf_from_html(fn_name_only, output_html, output_fn, css)

    # cleanup 
    if not options.save_buildfile and os.path.isdir(buildfiles_dir):
        shutil.rmtree(buildfiles_dir)


# if __name__ == '__main__':
#     lwm_to_pdf()