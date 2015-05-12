#!/bin/sh

# uses pdftk to burst multipage pdfs into singlepage pdfs

files="./*.pdf"

# run in the dir where the multipage pdfs are
for filename in $files
do
    base=${filename%.pdf}
    pdftk $filename burst output $base"-%04d.pdf"
done
