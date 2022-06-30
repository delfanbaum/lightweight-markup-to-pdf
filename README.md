# Lightweight Markup to PDF Builder

`lwm2pdf` is a Python script for building lightweight markup content into styled PDFs via 
[WeasyPrint](https://weasyprint.org/). 

To install:

```
pip install lwm2pdf
```

Basic usage:

```
lwm2pdf -i myfile.adoc --open y
```


## Requirements

See _pyproject.toml_ for Python requirements. For optimal asciidoc conversion, I strongly recommend that you install some version of [Asciidoctor](https://asciidoctor.org/) for asciidoc conversion, but a port of the original `asciidoc` converter is used as a backup.  

## Supported Filetypes

Currently, `lwm2pdf` supports the following filetypes:

- Asciidoc (_.adoc_ or _.asciidoc_)
- Markdown (_.md_)

## Options

| Option | Description | Required? |
|--------|-------------|-----------|
| `-i`, `--input` | The file to convert (full or relative path) |  True |
| `-o`, `--output` | Output filename and destination (optional) |  False |
| `-od`,`--output-dir` | Output directory and destination (optional); not recommended for use with the `-o` option |  False |
| `-s`, `--stylesheet` | Select user stylesheet (css) (optional) |  False |
| `-p`, `--preserve-buildfiles` | Preserve buildfiles in output/src in current working directory or buildfile directory | False |
| `-b`',`--buildfile-dir` | Destination for buildfile(s) directory | False |
| `--open` | "y" or "n" to automatically open or not open the pdf (doesn't ask) | `'ask'` |

## Stylesheets and Themes

A "manuscript" stylesheet is provided and selected as default. 


## Known Issues

Some known issues include:

- Table handling is not the best
- All footnotes are rendered as end notes (this is a constraint from WeasyPrint)
- Markdown support is spotty
- Code highlighting is not working as expected
- Image URIs have to be absolute paths for Weasyprint to process them successfully. The script will take care of that...eventually.

## Release Notes

### v.0.1.3

- Add description for pypy page

### v.0.1.2

- First release to pypi
- Includes many more tests (~82% coverage)
- Removes handling of smart quotes due to bugs (noted for future development)
- Move to a Poetry-based workflow
