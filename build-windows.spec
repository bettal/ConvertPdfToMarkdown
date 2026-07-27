# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_submodules

block_cipher = None

pymupdf_datas, pymupdf_binaries, pymupdf_hidden = collect_all('pymupdf')
pyqt6_datas, pyqt6_binaries, pyqt6_hidden = collect_all('PyQt6')
llm_hidden = collect_submodules('pymupdf4llm')

a = Analysis(
    ['pdf2md_gui/app.py'],
    pathex=['.'],
    binaries=pymupdf_binaries + pyqt6_binaries,
    datas=[
        ('icons/hicolor/256x256/apps/convert-pdf-to-markdown.png', 'icons'),
    ] + pymupdf_datas + pyqt6_datas,
    hiddenimports=[
        'fitz',
        'pymupdf',
        'pymupdf4llm',
    ] + pymupdf_hidden + pyqt6_hidden + llm_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'PyQt5',
        'PySide2',
        'PySide6',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ConvertPdfToMarkdown',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ConvertPdfToMarkdown',
)
