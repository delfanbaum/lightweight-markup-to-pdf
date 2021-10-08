# Lightweight Markup to PDF Builder

A Python script to build lightweight markup content (currently asciidoc and markdown to come) into a styled PDF (via weasyprint)

This is a work in progress! 

For Python requirements, see requirements.txt. Asciidoctor is also required, as is sass.

Note(s) to self:
- Project structure is a problem but lets try https://docs.python-guide.org/writing/structure/

Wishlist: 
- user stylesheet as argument 
-- rip out sass step; can just go with css and keep the sass for repo builds
- argument to include build output or not