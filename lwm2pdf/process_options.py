import os
import pkg_resources
from os.path import abspath


def get_fn_information(opt_input: str):
    """ takes options.input and returns a list of useful fn info """
    fn_name_only = opt_input.split("/")[-1].split('.')[0]
    return opt_input, fn_name_only


def get_output_information(options, fn_name_only):
    """ takes options.output and returns output filename """
    if options.output:
        if not options.output[-4:] == '.pdf':
            print('Error: Your output filetype must be ".pdf"')
            exit()
        else:
            output_fn = abspath(options.output)
    elif options.output_dir:
        if options.output_dir[-1] == '/':
            output_fn = f'{options.output_dir}{fn_name_only}.pdf'
        else:
            output_fn = f'{options.output_dir}/{fn_name_only}.pdf'
    else:
        print("Using default output destination...")
        output_fn = os.getcwd() + f'/{fn_name_only}.pdf'

    # get build directory
    if options.buildfile_dir:
        buildfiles_dir = abspath(options.buildfile_dir)
    else:
        buildfiles_dir = os.getcwd() + f'/{fn_name_only}-src'
    if not os.path.isdir(buildfiles_dir):
        # no longer cleaning b/c it'll just overwrite anyway
        os.mkdir(buildfiles_dir)

    output_html = f'{buildfiles_dir}/{fn_name_only}-buildfile.html'

    return output_fn, buildfiles_dir, output_html


def get_stylesheet_from_options(options):
    """ get the stylesheet or return default """
    if options.stylesheet:
        css = abspath(options.stylesheet)
    else:  # defaults
        print("Using default stylesheet...")
        css = pkg_resources.resource_filename('lwm2pdf',
                                              'themes/manuscript.css')
    return css
