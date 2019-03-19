#!/usr/bin/env python2

#from gimpfu import *

def enhance_sheetmusic(inpath, outpath):#, bx=9, by=9,azimuth=135, elevation=45, depth=3):
    import os
    import tempfile
    from subprocess import check_output, Popen
    img = pdb.file_png_load(inpath, inpath)
    drawable = pdb.gimp_image_get_active_drawable(img)
    
    width = drawable.width
    height = drawable.height

    img.disable_undo()

    filename = pdb.gimp_image_get_filename(img)
    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)

    #pdb.gimp_image_scale_full(img, 2*width, 2*height, 3) # 3 for NOHALO interpolation
    # convert to grayscale
    if pdb.gimp_image_base_type(img) != 1: # if its not grayscale already
        pdb.gimp_image_convert_grayscale(img)
    pdb.gimp_drawable_curves_explicit(drawable, 0, 256, [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.010096,0.030712,0.060704,0.098932,0.144253,0.195526,0.25161,0.311362,0.373641,0.437304,0.501211,0.564219,0.625188,0.682974,0.736436,0.784433,0.825823,0.859464,0.884214,0.894531,0.907747,0.920334,0.932305,0.943669,0.954441,0.96463,0.97425,0.983311,0.991826,0.999807,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0])

    # export as png
    # filename = os.path.join(dirname, "e-" + basename)
    # pdb.file_png_save_defaults(img,drawable,filename,filename)
    pdb.file_png_save_defaults(img,drawable,outpath,outpath)
    pdb.gimp_image_delete(img)
                      
# GIMP auto-execution stub
if __name__ == "__main__":
    import os, sys, subprocess
    # if len(sys.argv) < 2:
    #     print("you must specify a function to execute!")
    #     sys.exit(-1)
    # scriptname = sys.argv[1]
    # args = sys.argv[2:]
    scriptname = "enhance_sheetmusic"
    args = sys.argv[1:]
    scrdir = os.path.dirname(os.path.realpath(__file__))
    scrname = os.path.splitext(os.path.basename(__file__))[0]
    shcode = "import sys;sys.path.insert(0, '" + scrdir + "');import " + scrname + ";" + scrname + "." + scriptname + str(tuple(args))
    shcode = "gimp --no-interface -idf --batch-interpreter python-fu-eval -b \"" + shcode + "\" -b \"pdb.gimp_quit(1)\""
    sys.exit(subprocess.call(shcode, shell=True))
else:
    from gimpfu import *
    
# register(
#         "python_fu_enhance_sheetmusic_noninteractive",
#         "Use grayscale mode, scale up to 400% resolution and apply a curve to enhance contrast.",
#         "Use grayscale mode, scale up to 400% resolution and apply a curve to enhance contrast.",
#         "Thomas Rometsch",
#         "Thomas Rometsch",
#         "2019",
#         "<Image>/Filters/SheetMusic/_Enhance_noninteractive...",
#         "RGB*, GRAY*",
#         [
#             (PF_STRING, "inpath", "Input file path", "tmp.png"),
#             (PF_STRING, "outpath", "Output file path", "tmp.png")
#                 # (PF_INT, "x_blur", "X blur", 9),
#                 # (PF_INT, "y_blur", "Y blur", 9),
#                 # (PF_INT, "azimuth", "Azimuth", 135),
#                 # (PF_INT, "elevation", "Elevation", 45),
#                 # (PF_INT, "depth", "Depth", 3)
#         ],
#         [],
#         enhance_sheetmusic_noninteractive)

# main()
