# pdf2md-gui — Graphical interface for PyMuPDF4LLM
# Copyright (C) 2025  stas
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import os
import traceback
import threading
from importlib.metadata import version

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QCheckBox,
    QSpinBox, QTextEdit, QFileDialog, QMessageBox, QGroupBox,
    QMenuBar
)
from PyQt6.QtCore import Qt, pyqtSignal

import pymupdf4llm


class PDFToMarkdownApp(QMainWindow):
    log_signal = pyqtSignal(str)
    conversion_done = pyqtSignal(str, str, str)  # status, title, message

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF to Markdown Converter")
        self.resize(720, 720)

        self.pdf_path = ""
        self.output_path = ""

        self.log_signal.connect(self._append_log)
        self.conversion_done.connect(self._on_conversion_done)

        self._create_menu()

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(12, 12, 12, 12)

        # PDF file
        pdf_group = QGroupBox("PDF File")
        pdf_row = QHBoxLayout(pdf_group)
        self.pdf_btn = QPushButton("Browse PDF...")
        self.pdf_btn.clicked.connect(self._browse_pdf)
        self.pdf_label = QLabel()
        self.pdf_label.setStyleSheet("color: gray")
        pdf_row.addWidget(self.pdf_btn)
        pdf_row.addWidget(self.pdf_label, 1)
        layout.addWidget(pdf_group)

        # Output file
        out_group = QGroupBox("Output")
        out_row = QHBoxLayout(out_group)
        self.out_btn = QPushButton("Save as...")
        self.out_btn.clicked.connect(self._browse_output)
        self.out_label = QLabel()
        self.out_label.setStyleSheet("color: gray")
        out_row.addWidget(self.out_btn)
        out_row.addWidget(self.out_label, 1)
        layout.addWidget(out_group)

        # Options
        opts_group = QGroupBox("Options")
        opts_grid = QVBoxLayout(opts_group)

        r0 = QHBoxLayout()
        r0.addWidget(QLabel("Pages (e.g. 1-5,7,10-N):"))
        self.pages_edit = QLineEdit()
        r0.addWidget(self.pages_edit)
        opts_grid.addLayout(r0)

        r1 = QHBoxLayout()
        r1.addWidget(QLabel("DPI:"))
        self.dpi_spin = QSpinBox()
        self.dpi_spin.setRange(72, 600)
        self.dpi_spin.setValue(150)
        r1.addWidget(self.dpi_spin)
        r1.addSpacing(12)
        r1.addWidget(QLabel("Image format:"))
        self.img_fmt = QComboBox()
        self.img_fmt.addItems(["png", "jpg", "jpeg", "webp"])
        r1.addWidget(self.img_fmt)
        r1.addStretch()
        opts_grid.addLayout(r1)

        r2 = QHBoxLayout()
        r2.addWidget(QLabel("Table strategy:"))
        self.table_strat = QComboBox()
        self.table_strat.addItems(["lines_strict", "lines", "text"])
        r2.addWidget(self.table_strat)
        r2.addSpacing(12)
        r2.addWidget(QLabel("Margins:"))
        self.margins_spin = QSpinBox()
        self.margins_spin.setRange(0, 200)
        self.margins_spin.setValue(0)
        r2.addWidget(self.margins_spin)
        r2.addSpacing(12)
        r2.addWidget(QLabel("Page width:"))
        self.pw_spin = QSpinBox()
        self.pw_spin.setRange(100, 2000)
        self.pw_spin.setValue(612)
        r2.addWidget(self.pw_spin)
        r2.addStretch()
        opts_grid.addLayout(r2)

        layout.addWidget(opts_group)

        # Flags
        flags_group = QGroupBox("Flags")
        flags_row = QHBoxLayout(flags_group)
        self.cb_write_img = QCheckBox("Write images to disk")
        self.cb_embed_img = QCheckBox("Embed images (base64)")
        self.cb_ignore_img = QCheckBox("Ignore images")
        self.cb_ignore_gfx = QCheckBox("Ignore graphics")
        flags_row.addWidget(self.cb_write_img)
        flags_row.addWidget(self.cb_embed_img)
        flags_row.addWidget(self.cb_ignore_img)
        flags_row.addWidget(self.cb_ignore_gfx)
        layout.addWidget(flags_group)

        flags2_group = QGroupBox()
        flags2_row = QHBoxLayout(flags2_group)
        flags2_row.setContentsMargins(0, 0, 0, 0)
        self.cb_page_chunks = QCheckBox("Page chunks")
        self.cb_force_text = QCheckBox("Force text")
        self.cb_force_text.setChecked(True)
        self.cb_show_progress = QCheckBox("Show progress")
        self.cb_show_progress.setChecked(True)
        self.cb_ignore_code = QCheckBox("Ignore code")
        flags2_row.addWidget(self.cb_page_chunks)
        flags2_row.addWidget(self.cb_force_text)
        flags2_row.addWidget(self.cb_show_progress)
        flags2_row.addWidget(self.cb_ignore_code)
        flags2_row.addStretch()
        layout.addWidget(flags2_group)

        # Convert button
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.clicked.connect(self._convert)
        layout.addWidget(self.convert_btn)

        # Log
        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout(log_group)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        layout.addWidget(log_group, 1)

    def _create_menu(self):
        menubar = self.menuBar()
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About", self._show_about)

    def _show_about(self):
        try:
            ver = version("convert-pdf-to-markdown")
        except Exception:
            ver = "1.0.2"
        QMessageBox.about(
            self,
            "About Convert PDF to Markdown",
            f"<b>Convert PDF to Markdown</b><br>"
            f"Version: {ver}<br>"
            f"Author: stas<br>"
            f"License: GNU AGPL v3<br><br>"
            f"<a href='https://github.com/bettal/ConvertPdfToMarkdown'>Repository</a>"
        )

    def _browse_pdf(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select PDF file", "", "PDF files (*.pdf);;All files (*.*)"
        )
        if path:
            self.pdf_path = path
            self.pdf_label.setText(path)
            if not self.output_path:
                self.output_path = os.path.splitext(path)[0] + ".md"
                self.out_label.setText(self.output_path)

    def _browse_output(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save markdown as", "", "Markdown files (*.md);;All files (*.*)"
        )
        if path:
            self.output_path = path
            self.out_label.setText(path)

    def _log(self, msg):
        self.log_signal.emit(msg)

    def _append_log(self, msg):
        self.log_text.append(msg)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )

    def _on_conversion_done(self, status, title, message):
        self.convert_btn.setEnabled(True)
        self.convert_btn.setText("Convert")
        if status == "success":
            QMessageBox.information(self, title, message)
        else:
            QMessageBox.critical(self, title, message)

    def _parse_pages(self, raw: str, total: int):
        if not raw.strip():
            return None
        result = []
        for part in raw.split(","):
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                a, b = part.split("-", 1)
                a = a.strip()
                b = b.strip()
                start = int(a) - 1 if a else 0
                end = total - 1 if b.upper() == "N" else int(b) - 1
                result.extend(range(start, end + 1))
            else:
                result.append(int(part) - 1)
        return sorted(set(r for r in result if 0 <= r < total))

    def _convert(self):
        if not self.pdf_path or not os.path.isfile(self.pdf_path):
            QMessageBox.critical(self, "Error", "Please select a valid PDF file.")
            return

        out = self.output_path or os.path.splitext(self.pdf_path)[0] + ".md"
        self.output_path = out
        self.out_label.setText(out)

        kwargs = {}
        pages_raw = self.pages_edit.text().strip()
        if pages_raw:
            kwargs["pages"] = pages_raw

        kwargs["dpi"] = self.dpi_spin.value()
        kwargs["image_format"] = self.img_fmt.currentText()
        kwargs["table_strategy"] = self.table_strat.currentText()
        kwargs["page_width"] = self.pw_spin.value()
        kwargs["margins"] = self.margins_spin.value()
        kwargs["write_images"] = self.cb_write_img.isChecked()
        kwargs["embed_images"] = self.cb_embed_img.isChecked()
        kwargs["ignore_images"] = self.cb_ignore_img.isChecked()
        kwargs["ignore_graphics"] = self.cb_ignore_gfx.isChecked()
        kwargs["page_chunks"] = self.cb_page_chunks.isChecked()
        kwargs["force_text"] = self.cb_force_text.isChecked()
        kwargs["show_progress"] = self.cb_show_progress.isChecked()
        kwargs["ignore_code"] = self.cb_ignore_code.isChecked()

        self.convert_btn.setEnabled(False)
        self.convert_btn.setText("Converting...")
        self.log_text.clear()

        thread = threading.Thread(
            target=self._run_conversion, args=(self.pdf_path, out, kwargs), daemon=True
        )
        thread.start()

    def _run_conversion(self, pdf, out, kwargs):
        try:
            self._log(f"Opening: {pdf}")
            self._log(f"Options: {kwargs}")

            pages_arg = kwargs.pop("pages", None)
            if pages_arg is not None:
                import pymupdf
                with pymupdf.open(pdf) as doc:
                    total = doc.page_count
                parsed = self._parse_pages(pages_arg, total)
                if parsed is not None:
                    kwargs["pages"] = parsed
                    self._log(f"Pages selected: {len(parsed)} of {total}")
                else:
                    self._log(f"All {total} pages selected")
            else:
                self._log("All pages selected")

            self._log(f"pymupdf4llm version: {pymupdf4llm.__version__}")
            self._log("Converting to Markdown...")
            md_text = pymupdf4llm.to_markdown(pdf, **kwargs)

            if not md_text:
                self._log("WARNING: Conversion returned empty result!")
                self._log("The PDF may be scanned images without OCR, or the DLL failed to load.")

            with open(out, "w", encoding="utf-8") as f:
                f.write(md_text)

            self._log(f"Done! Saved to: {out}")
            self._log(
                f"Output size: {len(md_text)} chars / "
                f"~{len(md_text.splitlines())} lines"
            )

            self.conversion_done.emit(
                "success", "Success",
                f"Converted successfully!\nSaved to:\n{out}"
            )

        except Exception as e:
            self._log(f"ERROR: {e}")
            self._log(f"TRACEBACK:\n{traceback.format_exc()}")
            self.conversion_done.emit("error", "Error", str(e))


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Convert PDF to Markdown")
    app.setDesktopFileName("convert-pdf-to-markdown")
    window = PDFToMarkdownApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
