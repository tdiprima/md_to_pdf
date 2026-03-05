import logging
import os
from pathlib import Path

import markdown
from weasyprint import HTML, CSS

logger = logging.getLogger(__name__)

# CSS that ensures emoji render correctly via system emoji fonts
STYLE = CSS(string="""
body {
    font-family:
        "DejaVu Sans",
        "Helvetica Neue",
        Arial,
        sans-serif,
        "Segoe UI Emoji",
        "Noto Color Emoji",
        "Noto Emoji";
    font-size: 14px;
    line-height: 1.6;
    margin: 40px;
    color: #222;
}

h1, h2, h3, h4, h5, h6 {
    font-family:
        "DejaVu Sans",
        "Helvetica Neue",
        Arial,
        sans-serif,
        "Segoe UI Emoji",
        "Noto Color Emoji",
        "Noto Emoji";
    margin-top: 1.2em;
    margin-bottom: 0.4em;
}

code, pre {
    font-family: "Courier New", monospace;
    background: #f4f4f4;
    padding: 2px 6px;
    border-radius: 3px;
}

pre code {
    display: block;
    padding: 10px;
}

blockquote {
    border-left: 4px solid #ccc;
    padding-left: 1em;
    color: #555;
    margin-left: 0;
}

table {
    border-collapse: collapse;
    width: 100%;
}

th, td {
    border: 1px solid #ccc;
    padding: 6px 12px;
    text-align: left;
}
""")

MD_EXTENSIONS = [
    "tables",
    "fenced_code",
    "codehilite",
    "toc",
    "nl2br",
    "sane_lists",
]


def markdown_to_html(md_text: str) -> str:
    body = markdown.markdown(md_text, extensions=MD_EXTENSIONS)
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>{body}</body>
</html>"""


def convert_file(md_path: Path, output_dir: Path) -> Path:
    """Convert a single Markdown file to PDF. Returns the output PDF path."""
    logger.info("Converting %s", md_path)
    md_text = md_path.read_text(encoding="utf-8")
    html = markdown_to_html(md_text)

    pdf_path = output_dir / (md_path.stem + ".pdf")
    HTML(string=html, base_url=str(md_path.parent)).write_pdf(
        pdf_path, stylesheets=[STYLE]
    )
    logger.info("Written %s", pdf_path)
    return pdf_path


def convert_directory(input_dir: Path, output_dir: Path) -> list[Path]:
    """Convert all *.md files in input_dir to PDFs in output_dir."""
    md_files = sorted(input_dir.glob("*.md"))
    if not md_files:
        logger.warning("No *.md files found in %s", input_dir)
        return []

    output_dir.mkdir(parents=True, exist_ok=True)
    results = []
    errors = []

    for md_path in md_files:
        try:
            pdf_path = convert_file(md_path, output_dir)
            results.append(pdf_path)
        except Exception:
            logger.exception("Failed to convert %s", md_path)
            errors.append(md_path)

    logger.info(
        "Done. Converted %d file(s), %d error(s).", len(results), len(errors)
    )
    return results
