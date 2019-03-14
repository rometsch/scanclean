#!/usr/bin/env bash

for IMG in $1/*.png; do
	NAME="${IMG%.*}"
	convert -page A4 \
	       	-border 300 \
	       	-bordercolor white \
	       	-monochrome \
		-compress Group4 \
		"$IMG" tmp.png
	convert -page A4 \
		tmp.png $NAME.pdf
	rm tmp.png
done
