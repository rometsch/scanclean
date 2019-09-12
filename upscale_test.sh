#!/usr/bin/env bash
# Test filters of image magick to upscale image to 200%
# from http://www.imagemagick.org/discourse-server/viewtopic.php?t=17447
IN=$1
mkdir -p out
convert $IN -filter point -resize 200% out/point.png
convert $IN -filter point -resize 200% \-unsharp 0x1 out/point_unsharp.png
convert $IN -filter box -resize 200% out/box.png
convert $IN -filter box -resize 200% \-unsharp 0x1 out/box_unsharp.png
convert $IN -filter triangle -resize 200% out/triangle.png
convert $IN -filter triangle -resize 200% \-unsharp 0x1 out/triangle_unsharp.png
convert $IN -filter hermite -resize 200% out/hermite.png
convert $IN -filter hermite -resize 200% \-unsharp 0x1 out/hermite_unsharp.png
convert $IN -filter lagrange -resize 200% out/lagrange.png
convert $IN -filter lagrange -resize 200% \-unsharp 0x1 out/lagrange_unsharp.png
convert $IN -filter lagrange -define filter:support=2.25 \-resize 200% out/lagrangesupport225.png
convert $IN -filter lagrange -define filter:support=2.25 \-resize 200% \-unsharp 0x1 out/lagrange_support225_unsharp.png
convert $IN -filter lagrange -define filter:support=2.5 \-resize 200% out/lagrangesupport250.png
convert $IN -filter lagrange -define filter:support=2.50 \-resize 200% \-unsharp 0x1 out/lagrange_support250_unsharp.png
convert $IN -filter lagrange -define filter:support=2.75 \-resize 200% out/lagrangesupport275.png
convert $IN -filter lagrange -define filter:support=2.75 \-resize 200% \-unsharp 0x1 out/lagrange_support275_unsharp.png
convert $IN -filter lagrange -define filter:support=3 \-resize 200% out/lagrangesupport300.png
convert $IN -filter lagrange -define filter:support=3 \-resize 200% \-unsharp 0x1 out/lagrange_support300_unsharp.png
convert $IN -filter lagrange -define filter:support=3.25 \-resize 200% out/lagrangesupport325.png
convert $IN -filter lagrange -define filter:support=3.25 \-resize 200% \-unsharp 0x1 out/lagrange_support325_unsharp.png
convert $IN -filter catrom -resize 200% out/catrom.png
convert $IN -filter catrom -resize 200% \-unsharp 0x1 out/catrom_unsharp.png
convert $IN -filter lanczos -resize 200% out/lanczos.png
convert $IN -filter lanczos -resize 200% \-unsharp 0x1 out/lanczos_unsharp.png
convert $IN -filter cubic -resize 200% out/cubic.png
convert $IN -filter cubic -resize 200% \-unsharp 0x1 out/cubic_unsharp.png
convert $IN -filter quadratic -resize 200% out/quadratic.png
convert $IN -filter quadratic -resize 200% \-unsharp 0x1 out/quadratic_unsharp.png
convert $IN -filter mitchell -resize 200% out/mitchell.png
convert $IN -filter mitchell -resize 200% \-unsharp 0x1 out/mitchell_unsharp.png
convert $IN -filter gaussian -resize 200% out/gaussian.png
convert $IN -filter gaussian -resize 200% \-unsharp 0x1 out/gaussian_unsharp.png
convert $IN -filter gaussian -define filter:support=1.25 \-resize 200% out/gaussiansupport125.png
convert $IN -filter gaussian -define filter:support=1.25 \-resize 200% \-unsharp 0x1 out/gaussiansupport125_unsharp.png
convert $IN -filter gaussian -define filter:blur=.75 \-resize 200% out/gaussianblur75.png
convert $IN -filter gaussian -define filter:blur=.75 \-resize 200% \-unsharp 0x1 out/gaussianblur75_unsharp.png
convert $IN -filter gaussian -define filter:sigma=.25 \-resize 200% out/gaussiansigma25.png
convert $IN -filter gaussian -define filter:sigma=.25 \-resize 200% \-unsharp 0x1 out/gaussiansigma25_unsharp.png
convert $IN -filter sinc -resize 200% out/sinc.png
convert $IN -filter sinc -resize 200% \-unsharp 0x1 out/sinc_unsharp.png
convert $IN -filter sinc -define filter:support=5 \-resize 200% out/sincsupport5.png
convert $IN -filter sinc -define filter:support=5 \-resize 200% \-unsharp 0x1 out/sincsupport5_unsharp.png
convert $IN -filter sinc -define filter:support=6 \-resize 200% out/sincsupport6.png
convert $IN -filter sinc -define filter:support=6 \-resize 200% \-unsharp 0x1 out/sincsupport6_unsharp.png
convert $IN -filter sinc -define filter:support=7 \-resize 200% out/sincsupport7.png
convert $IN -filter sinc -define filter:support=7 \-resize 200% \-unsharp 0x1 out/sincsupport7_unsharp.png
convert $IN -filter sinc -define filter:support=8 \-resize 200% out/sincsupport8.png
convert $IN -filter sinc -define filter:support=8 \-resize 200% \-unsharp 0x1 out/sincsupport8_unsharp.png
convert $IN -filter spline -resize 200% out/spline.png
convert $IN -filter spline -resize 200% -unsharp 0x1 out/spline_unsharp.png

