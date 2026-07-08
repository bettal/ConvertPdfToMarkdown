# pdf2md-gui — Project Knowledge Base

## Description
GUI for PyMuPDF4LLM — converts PDF to Markdown with PyQt6 interface.

## Package info
- **Package name:** `convert-pdf-to-markdown`
- **Binary:** `/usr/bin/convert-pdf-to-markdown`
- **Desktop entry:** `/usr/share/applications/convert-pdf-to-markdown.desktop`
- **Menu category:** Development (KDE Plasma / GNOME)

## Project structure
```
ConvertPdfToMarkdown/
├── pdf2md_gui/         # Python package (main app in app.py)
├── debian/             # Debian packaging
│   ├── control         # Package metadata, deps
│   ├── changelog       # Version history
│   ├── postinst        # Post-install: pymupdf4llm compat check
│   ├── rules           # Build rules (dh)
│   ├── install         # File install mapping
│   ├── convert-pdf-to-markdown.desktop  # KDE/GNOME menu entry
│   ├── convert-pdf-to-markdown-launcher  # Shell launcher
│   ├── bump-version.sh # Auto version bump
│   └── postinst        # Post-install script
├── icons/              # Application icons (Candy Icons style)
│   └── hicolor/
│       ├── scalable/apps/   # SVG source
│       ├── 48x48/apps/      # PNG 48px (menu)
│       └── 256x256/apps/    # PNG 256px (window/taskbar)
├── dist/               # Built .deb packages
├── Makefile            # Build & release automation
├── setup.py            # Python package metadata
└── AGENTS.md           # This file
```

## Build commands
```bash
make build              # Build .deb (output goes to dist/)
make bump-patch         # Increment patch version + update files
make bump-minor         # Increment minor version
make bump-major         # Increment major version
make release            # bump-patch + build (default)
make VERSION=minor release  # bump-minor + build
```

Manual build:
```bash
dpkg-buildpackage -b -uc -us
mv ../convert-pdf-to-markdown_*.deb ../convert-pdf-to-markdown_*.buildinfo ../convert-pdf-to-markdown_*.changes dist/
```

## Key dependencies (runtime)
- python3-pyqt6
- python3-pymupdf (apt) — upgraded to latest via pip in postinst
- python3-pip (for pymupdf4llm upgrade)

## Post-install logic (debian/postinst)
1. Fetch latest pymupdf4llm version from PyPI
2. `pip install --upgrade --ignore-installed` (flag avoids debian pymupdf conflict)
3. Compatibility test: create temp PDF, convert via pymupdf4llm
4. On failure — fall back to apt version

## Version management
- `setup.py` and `debian/changelog` must stay in sync
- `debian/bump-version.sh` updates both
- Changelog follows debian format for `dpkg-buildpackage`

## Known issues
- debian-provided PyMuPDF can't be uninstalled by pip (no RECORD file)
  → fixed with `--ignore-installed` flag
- postinst uses `set -e` → all commands must tolerate failure or use `|| true`
