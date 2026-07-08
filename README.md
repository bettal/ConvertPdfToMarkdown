# pdf2md-gui

Graphical interface for [PyMuPDF4LLM](https://github.com/pymupdf/pymupdf4llm) — convert PDF files to Markdown.

## Features

- Select PDF and output file via dialogs
- Configure pages, DPI, image format, table strategy, margins
- Toggle image writing/embedding/ignoring
- Page chunks, force text, show progress, ignore code
- Conversion runs in background thread (UI stays responsive)
- Automatic `pymupdf4llm` version check and compatibility test on install

## Requirements

- Python 3.10+
- PyQt6
- pymupdf4llm (auto-checked on .deb install)

## Installation

### Debian package

```bash
sudo dpkg -i pdf2md-gui_1.0.0-1_all.deb
sudo apt-get install -f  # install dependencies
```

### Direct (via pip)

```bash
pip install -e .
pdf2md-gui
```

### Run without install

```bash
python3 -m pdf2md_gui.app
```

## License

Copyright (C) 2025 stas

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

This project is based on [PyMuPDF4LLM](https://github.com/pymupdf/pymupdf4llm)
by Artifex Software, Inc., also licensed under AGPL v3.
