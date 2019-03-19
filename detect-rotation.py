#!/usr/bin/env python3
import numpy as np
import cv2
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('-s', '--show', default=False, action="store_true",
                        help="show the detected lines on the image")
    parser.add_argument('-v', '--verbose', default=False, action="store_true")
    parser.add_argument('-c', '--correction', default=False,
                        action='store_true',
                        help="Output the angle to correct the image, i.e. the rotation angle times -1")
    args = parser.parse_args()

    rotation = get_rotation(args.file, ret_img=True,
                                 verbose=args.verbose,
                                 show=args.show)
    
    if args.correction:
        rotation *= -1
    print(rotation)


def get_rotation(filename, ret_img=False,
                 verbose=False, show=False):
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 7)
    L = img.shape[1]
    if verbose:
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
        if np.abs(alpha) > 10*np.pi/180:
            continue
        alphas.append(alpha)

    rotation = np.mean(alphas)/np.pi*180

    if show:
        cv2.imshow('edges', edges)
        cv2.imshow('result', img)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return rotation

if __name__=="__main__":
    main()
