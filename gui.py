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

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import pymupdf4llm


class PDFToMarkdownApp:
    def __init__(self, root):
        self.root = root
        root.title("PDF to Markdown Converter")
        root.geometry("700x750")
        root.minsize(600, 650)

        self.pdf_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.pages = tk.StringVar()
        self.dpi = tk.IntVar(value=150)
        self.image_format = tk.StringVar(value="png")
        self.table_strategy = tk.StringVar(value="lines_strict")
        self.margins = tk.StringVar(value="0")
        self.page_width = tk.IntVar(value=612)

        self.write_images = tk.BooleanVar(value=False)
        self.embed_images = tk.BooleanVar(value=False)
        self.ignore_images = tk.BooleanVar(value=False)
        self.ignore_graphics = tk.BooleanVar(value=False)
        self.page_chunks = tk.BooleanVar(value=False)
        self.force_text = tk.BooleanVar(value=True)
        self.show_progress = tk.BooleanVar(value=True)
        self.ignore_code = tk.BooleanVar(value=False)

        self._build_ui()

    def _build_ui(self):
        # File selection
        file_frame = ttk.LabelFrame(self.root, text="PDF File", padding=10)
        file_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        ttk.Button(file_frame, text="Browse PDF...", command=self._browse_pdf).pack(
            side=tk.LEFT, padx=(0, 10)
        )
        ttk.Label(file_frame, textvariable=self.pdf_path, foreground="gray").pack(
            side=tk.LEFT, fill=tk.X, expand=True
        )

        # Output file
        out_frame = ttk.LabelFrame(self.root, text="Output", padding=10)
        out_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(out_frame, text="Save as...", command=self._browse_output).pack(
            side=tk.LEFT, padx=(0, 10)
        )
        ttk.Label(out_frame, textvariable=self.output_path, foreground="gray").pack(
            side=tk.LEFT, fill=tk.X, expand=True
        )

        # Options
        opts = ttk.LabelFrame(self.root, text="Options", padding=10)
        opts.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Row 0: Pages, DPI
        r0 = ttk.Frame(opts)
        r0.pack(fill=tk.X, pady=2)
        ttk.Label(r0, text="Pages (e.g. 1-5,7,10-N):", width=25, anchor=tk.W).pack(
            side=tk.LEFT
        )
        ttk.Entry(r0, textvariable=self.pages).pack(side=tk.LEFT, fill=tk.X, expand=True)

        r1 = ttk.Frame(opts)
        r1.pack(fill=tk.X, pady=2)
        ttk.Label(r1, text="DPI:", width=25, anchor=tk.W).pack(side=tk.LEFT)
        ttk.Entry(r1, textvariable=self.dpi, width=10).pack(side=tk.LEFT)
        ttk.Label(r1, text="  Image format:").pack(side=tk.LEFT, padx=(10, 0))
        ttk.Combobox(
            r1, textvariable=self.image_format, values=["png", "jpg", "jpeg", "webp"],
            state="readonly", width=8
        ).pack(side=tk.LEFT)

        r2 = ttk.Frame(opts)
        r2.pack(fill=tk.X, pady=2)
        ttk.Label(r2, text="Table strategy:", width=25, anchor=tk.W).pack(side=tk.LEFT)
        ttk.Combobox(
            r2, textvariable=self.table_strategy,
            values=["lines_strict", "lines", "text"],
            state="readonly", width=15
        ).pack(side=tk.LEFT)
        ttk.Label(r2, text="  Margins:").pack(side=tk.LEFT, padx=(10, 0))
        ttk.Entry(r2, textvariable=self.margins, width=10).pack(side=tk.LEFT)

        r3 = ttk.Frame(opts)
        r3.pack(fill=tk.X, pady=2)
        ttk.Label(r3, text="Page width:", width=25, anchor=tk.W).pack(side=tk.LEFT)
        ttk.Entry(r3, textvariable=self.page_width, width=10).pack(side=tk.LEFT)

        # Checkboxes
        cb_frame = ttk.LabelFrame(self.root, text="Flags", padding=10)
        cb_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Checkbutton(cb_frame, text="Write images to disk",
                        variable=self.write_images).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Checkbutton(cb_frame, text="Embed images (base64)",
                        variable=self.embed_images).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Checkbutton(cb_frame, text="Ignore images",
                        variable=self.ignore_images).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Checkbutton(cb_frame, text="Ignore graphics",
                        variable=self.ignore_graphics).pack(side=tk.LEFT)

        cb_frame2 = ttk.Frame(self.root)
        cb_frame2.pack(fill=tk.X, padx=20, pady=(0, 5))

        ttk.Checkbutton(cb_frame2, text="Page chunks",
                        variable=self.page_chunks).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Checkbutton(cb_frame2, text="Force text",
                        variable=self.force_text).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Checkbutton(cb_frame2, text="Show progress",
                        variable=self.show_progress).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Checkbutton(cb_frame2, text="Ignore code",
                        variable=self.ignore_code).pack(side=tk.LEFT)

        # Convert button
        self.convert_btn = ttk.Button(
            self.root, text="Convert", command=self._convert
        )
        self.convert_btn.pack(pady=10)

        # Progress / log area
        log_frame = ttk.LabelFrame(self.root, text="Log", padding=5)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.log_text = tk.Text(log_frame, height=10, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def _browse_pdf(self):
        path = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if path:
            self.pdf_path.set(path)
            default_out = os.path.splitext(path)[0] + ".md"
            if not self.output_path.get():
                self.output_path.set(default_out)

    def _browse_output(self):
        path = filedialog.asksaveasfilename(
            title="Save markdown as",
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
        )
        if path:
            self.output_path.set(path)

    def _log(self, msg):
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)
        self.root.update_idletasks()

    def _parse_pages(self, raw: str, total: int):
        if not raw.strip():
            return None
        result = []
        parts = raw.split(",")
        for part in parts:
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                a, b = part.split("-", 1)
                a = a.strip()
                b = b.strip()
                start = int(a) - 1 if a else 0
                if b.upper() == "N":
                    end = total - 1
                else:
                    end = int(b) - 1
                result.extend(range(start, end + 1))
            else:
                result.append(int(part) - 1)
        return sorted(set(r for r in result if 0 <= r < total))

    def _convert(self):
        pdf = self.pdf_path.get()
        if not pdf or not os.path.isfile(pdf):
            messagebox.showerror("Error", "Please select a valid PDF file.")
            return

        out = self.output_path.get()
        if not out:
            out = os.path.splitext(pdf)[0] + ".md"
            self.output_path.set(out)

        kwargs = {}
        if self.pages.get().strip():
            kwargs["pages"] = self.pages.get().strip()

        kwargs["dpi"] = self.dpi.get()
        kwargs["image_format"] = self.image_format.get()
        kwargs["table_strategy"] = self.table_strategy.get()
        kwargs["page_width"] = self.page_width.get()

        margins_str = self.margins.get().strip()
        if margins_str:
            try:
                kwargs["margins"] = float(margins_str)
            except ValueError:
                kwargs["margins"] = 0

        kwargs["write_images"] = self.write_images.get()
        kwargs["embed_images"] = self.embed_images.get()
        kwargs["ignore_images"] = self.ignore_images.get()
        kwargs["ignore_graphics"] = self.ignore_graphics.get()
        kwargs["page_chunks"] = self.page_chunks.get()
        kwargs["force_text"] = self.force_text.get()
        kwargs["show_progress"] = self.show_progress.get()
        kwargs["ignore_code"] = self.ignore_code.get()

        self.convert_btn.configure(state=tk.DISABLED, text="Converting...")
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state=tk.DISABLED)

        thread = threading.Thread(
            target=self._run_conversion, args=(pdf, out, kwargs), daemon=True
        )
        thread.start()

    def _run_conversion(self, pdf, out, kwargs):
        try:
            self._log(f"Opening: {pdf}")

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

            self._log("Converting to Markdown...")
            md_text = pymupdf4llm.to_markdown(pdf, **kwargs)

            with open(out, "w", encoding="utf-8") as f:
                f.write(md_text)

            self._log(f"Done! Saved to: {out}")
            self._log(f"Output size: {len(md_text)} chars / ~{len(md_text.splitlines())} lines")

            self.root.after(0, lambda: messagebox.showinfo(
                "Success", f"Converted successfully!\nSaved to:\n{out}"
            ))

        except Exception as e:
            self._log(f"ERROR: {e}")
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            self.root.after(0, lambda: self.convert_btn.configure(
                state=tk.NORMAL, text="Convert"
            ))


def main():
    root = tk.Tk()
    app = PDFToMarkdownApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
