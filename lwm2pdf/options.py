import argparse

# options parsing
def get_lwm2pdf_options(supperted_file_types: str):
    cli_options_parser = argparse.ArgumentParser(prog='lwm2pdf',
                        usage='%(prog)s [options]',
                        description=f'Converts {supperted_file_types} into PDFs based on default or user stylesheet (css).')

    cli_options_parser.add_argument('-i', '--input', 
                                    dest='input',
                                    action='store',
                                    type=str, 
                                    required=True,
                                    help=f'the file to convert ({supperted_file_types})')

    cli_options_parser.add_argument('-o', '--output',
                                    dest='output',
                                    type=str,
                                    required=False,
                                    help='output filename and destination (optional)')

    cli_options_parser.add_argument('-s', '--stylesheet',
                                    dest='stylesheet',
                                    type=str,
                                    required=False,
                                    help='select user stylesheet (css) (optional)')
    cli_options_parser.add_argument('-p', '--preserve-buildfiles',
                                    action="store_true",
                                    required=False,
                                    help='preserve buildfiles in output/src in current working directory')


    return cli_options_parser.parse_args()
