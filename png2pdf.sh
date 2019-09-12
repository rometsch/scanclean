#!/usr/bin/env bash

TMPDIR="$(mktemp -d)"
TMPFILE="$TMPDIR/tmp.png"

IMG="$1"
NAME="${IMG%.*}"
#convert "$IMG" -page A4 -gravity center -stroke white -bordercolor white -border 300 "$TMPFILE"
convert -border 300 \
		-bordercolor white \
		"$IMG" "$TMPFILE"
	    #-monochrome \
		#-compress Group4
convert -page A4 -format pdf "$TMPFILE"  "$NAME.pdf"

#rm -rf $TMPDIR
echo "png2pdf $TMPDIR"
