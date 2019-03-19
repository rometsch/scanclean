#!/usr/bin/env bash
SCRIPTDIR="$(dirname $(realpath $0))"
echo $SCRIPTDIR
GETROTATION="$SCRIPTDIR/detect-rotation.py -c"
CORRECTIONANGLE="$($GETROTATION $1)"
echo "$(basename $1) : $CORRECTIONANGLE"
convert -rotate $CORRECTIONANGLE "$1" "rot-$1"
