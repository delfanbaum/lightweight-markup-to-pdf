from lwm2pdf.options import get_lwm2pdf_options
from lwm2pdf.main import supported_file_types
from lwm2pdf.process_options import get_fn_information
import pytest


@pytest.fixture
def testing_options():
    fn = "example.adoc"
    return ['-i', fn]


class TestOptionResults:
    """
    Tests that we get the correct outputs from options
    """

    def test_input_filename(self, testing_options):
        """ confirms the correct things happen to the -i flag"""
        fn = "example.adoc"
        options = get_lwm2pdf_options(supported_file_types, testing_options) 
        assert options.input == fn

    def test_get_fn(self, example="random/path/to/file.asciidoc"):
        opt_input, fn_name = get_fn_information(example)
        assert opt_input == example
        assert fn_name == 'file'
