import os
from os.path import abspath


def get_fn_information(opt_input: str):
    """ takes options.input and returns a list of useful fn info """
    fn_full_path = abspath(opt_input)
    fn_name_only = opt_input.split("/")[-1].split('.')[0]
    return opt_input, fn_full_path, fn_name_only


def get_output_fn_information(options, fn_name_only):
    """ takes options.output and returns output filename """
    if options.output:
        if not options.output[-4:] == '.pdf':
            print('Error: Your output filetype must be ".pdf"')
            exit()
        else:
            output_fn = abspath(options.output)
    elif options.output_dir:
        if options.output_dir[-1] == '/':
            output_fn = os.getcwd() + \
                        f'/{options.output_dir}{fn_name_only}.pdf'
        else:
            output_fn = os.getcwd() + \
                        f'/{options.output_dir}/{fn_name_only}.pdf'
    else:
        print("Using default output destination...")
        output_fn = os.getcwd() + f'/{fn_name_only}.pdf'

    return output_fn


def get_stylesheet_from_options(options):
    """ get the stylesheet or return default """
    if options.stylesheet:
        css = abspath(options.stylesheet)
    else:  # defaults
        print("Using default stylesheet...")
        script_dir = os.path.dirname(__file__)
        script_home = str(os.path.abspath(script_dir))
        styles_home = ('/').join(script_home.split('/')[0:-1])
        css = styles_home + '/themes/manuscript.css'
    return css
