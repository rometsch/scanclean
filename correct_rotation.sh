#!/usr/bin/env bash
SCRIPTDIR="$(dirname $(realpath $0))"
echo $SCRIPTDIR
GETROTATION="$SCRIPTDIR/detect-rotation.py -c"
CORRECTIONANGLE="$($GETROTATION $1)"
echo "$(basename $1) : $CORRECTIONANGLE"

if [[ "$#" > 1 ]]; then
	OUTPATH="$2"
else
	OUTPATH="rot-$1"
fi

convert -rotate $CORRECTIONANGLE "$1" "$OUTPATH"
