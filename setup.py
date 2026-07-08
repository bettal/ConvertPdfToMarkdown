from setuptools import setup, find_packages

setup(
    name="convert-pdf-to-markdown",
    version="1.0.3",
    description="Graphical interface for PyMuPDF4LLM — convert PDF to Markdown",
    long_description=open("README.md").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="stas",
    url="https://github.com/bettal/ConvertPdfToMarkdown",
    license="GNU AGPL v3",
    license_files=["LICENSE"],
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "PyQt6",
        "pymupdf4llm>=1.28.0",
    ],
    entry_points={
        "console_scripts": [
            "convert-pdf-to-markdown=pdf2md_gui.app:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Natural Language :: Russian",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
)
