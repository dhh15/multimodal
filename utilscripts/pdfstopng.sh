#!/bin/bash

# pdfs to pngs

files="./singlepagepdfs/*.pdf"
outdir="./singelpagepngs/"

# run in the dir where the multipage pdfs are
for filename in $files
do
    base=${filename%.pdf}
    echo  "$outdir$base.png"
    convert -density 300 $filename "$outdir$base.png"
done
