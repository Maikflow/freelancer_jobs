txt_image.py
----------------------------------
Script that takes a input and an output directories as arguments.
Reads all text files in input directory(files shoud be as in "indir"
folder of a folder this program is in) and converts
thet to a diagram(plot) with transparent background(png format).
File names of output files are the same as
input files, except for the extentions.

Usage (works with both python 2 and pyhton 3):
	python txt_image.py -i input_dir -o output_dir

Note: you will need Matplotlib library installed to run this program.

If no input_dir was provided, current working directory will be used.
If no output_dir was provided, it will be equal to input_dir.