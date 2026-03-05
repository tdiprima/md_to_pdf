# md to pdf

I want to convert long Markdown documents into PDFs so we get things like page numbers, bookmarks, and other document navigation features.

Using WeasyPrint (HTML/CSS → PDF renderer) with emoji-supporting fonts. The approach: Markdown → HTML → PDF with a CSS font stack that includes emoji fonts.

## Install:

```sh
pip install -r md_to_pdf/requirements.txt
```

WeasyPrint also needs system libraries. On macOS:

```sh
brew install pango
```

## Usage:
```sh
# PDFs written alongside the .md files
python main.py /path/to/your/docs

# PDFs written to a separate output folder
python main.py /path/to/your/docs --output-dir /path/to/pdfs
```

### How emoji support works:

The CSS font stack in converter.py lists "Apple Color Emoji" first on macOS, then falls back to "Segoe UI Emoji" (Windows) and "Noto Color Emoji" (Linux). 

WeasyPrint uses these system fonts when rendering the HTML, so emoji characters in your Markdown render as color glyphs in the PDF.

On Linux, if emojis appear as boxes, install the Noto Emoji font:

```sh
sudo apt install fonts-noto-color-emoji # Debian/Ubuntu
```

<br>
