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
parser.add_argument("directory", help="directory containing the youtube snapshots");
parser.add_argument("--dry", action='store_const', const=True, default=False , help="dryrun, only generate image list");
parser.add_argument("--clean", action='store_const', const=True, default=False , help="use textcleaner script for some intermediate steps");
parser.add_argument("--skip-clut", action='store_const', const=True, default=False , help="skip applying the clut image to leave the image full grayscale");
parser.add_argument("--crop", default="2400x1800+240", help="crop argument passed to imagemagicks convert command");
parser.add_argument("--magnify", default=1, type=int, help="number of times to apply the magnify option");
parser.add_argument("-c","--cutoff", default = "0.8", help="position of the soft cut-off");
parser.add_argument("-w","--width", default = "0.015" , help="width of the soft cut-off");
args = parser.parse_args();

directory = args.directory;
textcleaner = os.path.join(os.getcwd(), "textcleaner");

gradientfile = os.path.join(directory, "gradient.png");
make_clut_image(args.cutoff, args.width, filepath=gradientfile);

filelist = "{";
cnt = 1;
for filename in os.listdir(directory):
	if "Bildschirmfoto" in filename: 
		infile = os.path.join(directory, filename);
		croppedfile = os.path.join(directory, "cropped{:03d}.png".format(cnt));
		magnifiedfile = os.path.join(directory, "mag{:03d}.png".format(cnt));
		outfile = os.path.join(directory, "{:03d}.png".format(cnt));
		tmpfile = os.path.join(directory, "tmp{:03d}.png".format(cnt));
		if filelist == "{":
			filelist += "{:03d}.png".format(cnt);
		else:
			filelist += ",{:03d}.png".format(cnt);
		print("Processing {:d}".format(cnt));
		cnt += 1;
		if not args.dry:
			CMD = ["convert", "-crop", args.crop, "-colorspace", "Gray", infile, outfile];
			call(CMD);
			CMD = ["magick", outfile] + ["-magnify"]*args.magnify + [outfile];
			call(CMD);
			if args.clean:
				CMD = [textcleaner, "-f", "15", "-o", "3", "-e", "normalize", "-t", "20", "-s", "2", outfile , tmpfile]
				call(CMD);
				CMD = ["convert", outfile, tmpfile, "-evaluate-sequence", "Min", outfile];
				call(CMD);
			if not args.skip_clut:
				CMD = ["convert", outfile, gradientfile, "-clut", outfile];
				call(CMD);
		continue
	else:
		continue
filelist += "}"
print(filelist);
with open(os.path.join(directory, "imagelist.txt"), "w") as f:
	print(filelist, file=f);
