from lwm2pdf.options import get_lwm2pdf_options
from lwm2pdf.process_options import (
        get_fn_information,
        get_output_fn_information
        )

supported_file_types = '*.adoc, *.asciidoc, or *.md'


def main():
    """
    This is the main function that takes us from CLI-provided
    arguments to a PDF
    """
    options = get_lwm2pdf_options(supported_file_types)
    
    fn, fn_path, fn_name = get_fn_information(options.input)
    output_fn = get_output_fn_information(options, fn_name) 


if __name__ == '__main__':
    main()
