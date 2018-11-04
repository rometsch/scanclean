#!/usr/bin/env python3
import numpy as np
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('-s', '--show', default=False, action="store_true",
                    help="show the detected lines on the image")
parser.add_argument('-v', '--verbose', default=False, action="store_true")
args = parser.parse_args()

img = cv2.imread(args.file)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 7)
L = img.shape[1]
if args.verbose:
    print("size = {}".format(img.shape))
minLineLength=L*0.5
lines = cv2.HoughLinesP(image=edges,
                        rho=1,
                        theta=np.pi/500,
                        threshold=int(0.1*L),
                        lines=np.array([]),
                        minLineLength=minLineLength,
                        maxLineGap=int(0.05*L))

alphas = []

a,b,c = lines.shape
for i in range(a):
    cv2.line(img, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
    dx = lines[i][0][0] - lines[i][0][2]
    dy = lines[i][0][1] - lines[i][0][3]
    alpha = np.arctan(dy/dx)
    #print("dx = {:.2f}, dy = {:.2f}, alpha = {:.2f}".format(dx, dy, alpha/np.pi*180))
    alphas.append(alpha)

rotation = np.mean(alphas)/np.pi*180
print(rotation)

if args.show:
    cv2.imshow('edges', edges)
    cv2.imshow('result', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
