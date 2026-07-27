# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['pdf2md_gui/app.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('icons/hicolor/256x256/apps/convert-pdf-to-markdown.png', 'icons'),
    ],
    hiddenimports=['pymupdf', 'fitz'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ConvertPdfToMarkdown',
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
)