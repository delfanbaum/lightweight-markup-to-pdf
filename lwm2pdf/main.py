import smartypants
from lwm2pdf.clean_html import clean_html
from lwm2pdf.options import get_lwm2pdf_options
from lwm2pdf.process_options import (
        get_fn_information,
        get_output_information,
        get_stylesheet_from_options
        )
from lwm2pdf.process_pdf import create_pdf, open_pdf
from lwm2pdf.process_docs import markup_to_html
from lwm2pdf.filetypes import supported_file_types


def lwm2pdf(args=None):
    """
    This is the main function that takes us from CLI-provided
    arguments to a PDF
    """
    # setup
    options = get_lwm2pdf_options(supported_file_types, args)
    fn, fn_name = get_fn_information(options.input)
    output_fn, build_dir, output_html = get_output_information(options,
                                                               fn_name)
    css = get_stylesheet_from_options(options)
    styles = open(css, 'r').read()

    # processing
    html = markup_to_html(fn, supported_file_types)
    html = clean_html(html)

    if options.run_smartypants:
        html = smartypants.smartypants(html)

    # create output for checking/pasting to word
    open(output_html, 'w').write(html)
    print(f"Writing styled output to {fn_name}_styled...")
    html_with_styles = html.replace('</head>',
                                    f'<style>{styles}</style></head>')
    open(output_html.replace('.html', "_styled.html"), 'w').write(
                html_with_styles
        )

    if create_pdf(fn, output_fn, build_dir, output_html, styles, options):
        open_pdf(output_fn, options.ask_to_open)


if __name__ == '__main__':  # type: ignore
    lwm2pdf()
