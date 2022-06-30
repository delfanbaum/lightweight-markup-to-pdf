from lwm2pdf.main import lwm2pdf
from os.path import exists
import pytest  # type: ignore


@pytest.fixture(scope="session")
def out_dir(tmp_path_factory):
    d = tmp_path_factory.mktemp("pdf")
    return str(d)


def test_lwm2pdf_happypath_adoc(out_dir,
                           test_file="tests/docs/manuscript.adoc"):
    output_name = test_file.split('/')[-1].split('.')[0]
    lwm2pdf(['-i', test_file, '-od', out_dir])  # type: ignore

    assert exists(f'{out_dir}/{output_name}.pdf')


def test_lwm2pdf_happypath_md(out_dir,
                           test_file="tests/docs/memo.md"):
    output_name = test_file.split('/')[-1].split('.')[0]
    lwm2pdf(['-i', test_file, '-od', out_dir])  # type: ignore

    assert exists(f'{out_dir}/{output_name}.pdf')


def test_lwm2pdf_artifacts(out_dir,
                           test_file="tests/docs/include.adoc"):
    output_name = test_file.split('/')[-1].split('.')[0]
    lwm2pdf(['-i', test_file,
             '-od', out_dir,
             '-b', f'{out_dir}/src',
             '-p'
             ])  # type: ignore

    assert exists(f'{out_dir}/{output_name}.pdf')
    assert exists(f'{out_dir}/src/{output_name}-buildfile_styled.html')
    assert exists(f'{out_dir}/src/{output_name}-buildfile.html')
