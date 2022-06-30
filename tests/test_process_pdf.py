import pytest
from lwm2pdf.process_pdf import open_pdf


def test_open_pdf_mac(fp):
    """ tests open pdf """
    fp.register(['open', "some.pdf"])
    assert open_pdf("some.pdf", "y") == ''
