#!/usr/bin/env python3

import argparse;
import os;
from subprocess import call;
import matplotlib.image as mpimg;
import numpy as np;

""" Construct an image which is used by image magick to map the colors imitating the GIMP color curve feature. """
def make_clut_image(cutoff_position,width,filepath="gradient.png"):
	c = float(cutoff_position);
	#w = float(width);
	w = 0.01
	""" Make a lookuptable image """
	# First sample the function.
	x = np.linspace(0.0,1.0,512);
	clut = 1.0/(1.0 + np.exp(- (x-c)/w ))
	# Second transform to a greyscale image array.
	img = np.array( [[[elem]] for elem in clut] ).repeat(4,1).repeat(4,2);
	# Set the alpha channel to 1.0;
	img[:,:,3] = 1.0;
	# Save clut image
	mpimg.imsave(filepath, img);
	
parser = argparse.ArgumentParser();
parser.add_argument("filename")
parser.add_argument("--skip-clut", action='store_const', const=True, default=False , help="skip applying the clut image to leave the image full grayscale");
parser.add_argument("--magnify", default=1, type=int, help="number of times to apply the magnify option");
parser.add_argument("-c","--cutoff", default = "0.8", help="position of the soft cut-off");
parser.add_argument("-w","--width", default = "0.015" , help="width of the soft cut-off");
args = parser.parse_args();


filename = args.filename
name = ".".join(os.path.basename(filename).split(".")[:-1])
directory = os.path.dirname(filename)
infile = os.path.join(directory, filename);
croppedfile = os.path.join(directory, "{}-cropped.png".format(name));
magnifiedfile = os.path.join(directory, "{}-mag.png".format(name));
outfile = os.path.join(directory, "{}-enhanced.png".format(name));
tmpfile = os.path.join(directory, "{}-tmp.png".format(name));

gradientfile = os.path.join(directory, "gradient.png");
make_clut_image(args.cutoff, args.width, filepath=gradientfile);


#CMD = ["magick", outfile] + ["-magnify"]*args.magnify + [outfile];
#call(CMD);
if not args.skip_clut:
	CMD = ["convert", filename, gradientfile, "-clut", outfile];
	call(CMD);
