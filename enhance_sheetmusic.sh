#!/usr/bin/env bash

TMPDIR="$PWD/tmp"
mkdir $TMPDIR
TMPFILE1="$TMPDIR/clean.png"
TMPFILE2="$TMPDIR/$(basename $1)"
./enhance_sheetmusic.py "$1" "$TMPFILE1"
ANGLE="$(~/repo/scanclean/detect-rotation.py -c $TMPFILE1)"
convert -rotate $ANGLE $TMPFILE1 $TMPFILE2
