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
                                    action='store',
                                    type=str,
                                    required=False,
                                    help='output filename and destination (optional)')

    cli_options_parser.add_argument('-od', '--output-dir',
                                    dest='output_dir',
                                    action='store',
                                    type=str,
                                    required=False,
                                    help='output filename and destination (optional)')

    cli_options_parser.add_argument('-s', '--stylesheet',
                                    dest='stylesheet',
                                    action='store',
                                    type=str,
                                    required=False,
                                    help='select user stylesheet (css) (optional)')
    cli_options_parser.add_argument('-p', '--preserve-buildfiles',
                                    dest="save_buildfile",
                                    action="store_true",
                                    required=False,
                                    help='preserve buildfiles in output/src in current working directory')
    cli_options_parser.add_argument('-bd', '--buildfile-dir',
                                    dest="buildfile_dir",
                                    action='store',
                                    type=str,
                                    required=False,
                                    help='destination for buildfile(s) directory')                                
    cli_options_parser.add_argument('--open',
                                    action='store',
                                    type=str,
                                    required=False,
                                    dest='ask_to_open')

    return cli_options_parser.parse_args()
