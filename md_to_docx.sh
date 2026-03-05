#!/bin/bash

for f in *.md; do
    pandoc -f markdown -t docx -o "$f.docx" "$f"
done
