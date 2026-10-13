#!/usr/bin/env python3
"""Convert all Markdown files in docs/ to PDF using md-to-pdf (Node.js)."""

import shutil
import subprocess
import pathlib

DOCS_DIR = pathlib.Path(__file__).parent
PDF_DIR = DOCS_DIR / "pdf"
PDF_DIR.mkdir(exist_ok=True)


def convert_markdown_to_pdf(md_file: pathlib.Path) -> pathlib.Path:
    """Convert a single Markdown file to PDF using md-to-pdf."""
    relative = md_file.relative_to(DOCS_DIR)
    out_file = PDF_DIR / relative.with_suffix(".pdf")
    out_file.parent.mkdir(parents=True, exist_ok=True)

    print(f"Converting: {relative}")

    # md-to-pdf outputs the PDF in the same directory as the input
    generated_pdf = md_file.with_suffix(".pdf")

    subprocess.run(
        ["npx", "--yes", "md-to-pdf", str(md_file.name)],
        cwd=str(md_file.parent),
        check=True,
        capture_output=True,
    )

    if generated_pdf.exists():
        shutil.move(str(generated_pdf), str(out_file))
    else:
        raise FileNotFoundError(f"Expected PDF not found: {generated_pdf}")

    return out_file


for md_file in sorted(DOCS_DIR.rglob("*.md")):
    if md_file.name == "convert_to_pdf.py":
        continue
    convert_markdown_to_pdf(md_file)

print(f"\nDone! PDFs saved to: {PDF_DIR}")
