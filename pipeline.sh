#!/usr/bin/env bash
# Full pipeline to correct a cropped sheet music image

SCRIPTDIR="$(dirname $(realpath $0))"
TMPDIR="$(mktemp -d)"

# Scale image up
convert "$1" -filter catrom -resize 200% \-unsharp 0x1 -colorspace Gray $TMPDIR/upscaled.png

# Enhance contrast
$SCRIPTDIR/enhance_edges.py --outfile $TMPDIR/enhanced.png $TMPDIR/upscaled.png

# Rotate the image
$SCRIPTDIR/correct_rotation.sh $TMPDIR/upscaled.png $TMPDIR/rotated.png

# make an A4 pdf
$SCRIPTDIR/png2pdf.sh $TMPDIR/enhanced.png

if [[ "$#" > 1 ]]; then
	OUTPATH="$2"
else
	OUTPATH="${1%.*}.pdf"
fi
	
cp $TMPDIR/enhanced.pdf "$OUTPATH"

#rm -rf $TMPDIR
echo "pipeline $TMPDIR"
