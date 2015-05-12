#!/bin/sh

#  wrapper for pdftotext


files="./*.pdf"

# run in the dir where the multipage pdfs are
for filename in $files
do
    pdftotext $filename
done
