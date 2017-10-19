#!/usr/local/bin/python3
import os;
from subprocess import call;
import matplotlib.image as mpimg;
import matplotlib.pyplot as plt;
import numpy as np;
import argparse;

convert_cmd = ["gm","convert"];

cwd = os.getcwd();

# Clut file path
clut_file_path = os.path.join(cwd,"clut.png");

def reduce_noise(in_path, out_path):
	pass

def rotate(files , angle):
	call( convert_cmd + [ files["in"], "rotate", angle, files["out"]] );

def scale(files, percentage = 400, filter=None):
	cmd = ["magick", files["in"], "-magnify", files["out"]];
	call(cmd);

""" Construct an image which is used by image magick to map the colors imitating the GIMP color curve feature. """
def make_clut_image(cutoff_position,width):
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
	mpimg.imsave("clut.png", img);


""" Apply the lookup table to the input image """
def enhance_contrast(files, cutoff_position, width):
	make_clut_image(cutoff_position, width);
	cmd = ["convert", files["in"], clut_file_path, "-clut", files["out"]];
	call(cmd, cwd=cwd);

""" Show an array to compare images """
def show_images(images, title = ""):
	num_images = len(images);
	num_hor = 2;
	num_vert = int(np.ceil(float(num_images)/num_hor));
	fig, axes = plt.subplots(num_vert,num_hor);
	for ax, img_path in zip(axes.ravel(), images):
		try:
			img = mpimg.imread(img_path);
			#ax.locator_param(tight=True);
			ax.imshow(img);
		except:
			pass;
	fig.suptitle(title);
	plt.show()


#--------------------------------------------------------------------------------
#	Parse command line arguments
#--------------------------------------------------------------------------------
parser = argparse.ArgumentParser();
parser.add_argument("-i","--inputfile", default = os.path.join(cwd, "testfield.png"), help="file to be enhanced");
parser.add_argument("-c","--cutoff", default = "0.8", help="position of the soft cutoff");
parser.add_argument("-w","--width", default = "0.015" , help="width of the soft cut off");
parser.add_argument("-f","--filter", default = "Cubic" , help="interpolation method");
args = parser.parse_args();

width = args.width;
cutoff_position = args.cutoff;

images = [];

in_path = os.path.abspath(args.inputfile);
filename_in = os.path.basename(in_path);
filename_parts = filename_in.rsplit(".",2);
basename = filename_parts[0];
extension = filename_parts[1];

""" Define the stages of processing. """
stages = {	"scale"		: { "suffix" : "scale"	,	"function" : lambda files : scale(files, filter = args.filter)	},
		"contrast"	: { "suffix" : "contrast",	"function" : lambda files : enhance_contrast(files, args.cutoff, args.width) } };
""" Make filenames for the temporary file for every stage. """
for st in stages:
	stages[st]["filename"] = "{}_{}.{}".format(basename, st, extension);

""" Make a list to set in which order to apply the stages. """
stages_order = ["scale", "contrast"];

""" Apply all stages to the input file and save a list with labels and filepaths. """
labels = ["input"];
files = [filename_in];
for st in stages_order:
	# Get the function to call in this stage
	f = stages[st]["function"];
	# Get the output filename for this stage
	filename = stages[st]["filename"];
	# Call the function for this stage
	f( { "in" : files[-1], "out" : filename} ); 
	# Append filename and label to list
	files.append(filename);
	labels.append(st);

show_images(files, "cutoff = {}, width = {}".format( args.cutoff, args.width))
