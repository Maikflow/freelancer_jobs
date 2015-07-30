import re
import os
import sys
from os import path
from os import listdir
import lorentz
import getopt

import numpy as np
import matplotlib.pyplot as plt
from pylab import grid

#import lorentzian
    
def process_dir(indir, outdir):
    """ Reads text files from indir and saves plot images into outdir. """
    
    success_count = 0
    fail_count = 0
    
    print("") # empty line
    
    for fname in listdir(indir):
        if not fname.endswith('.txt'):
            continue
        
        readfilepath = path.join(indir, fname)
        savename = "%s.png" % os.path.splitext(fname)[0]
        savefilepath = path.join(outdir, savename)
        
        print("Processing file '%s':" % fname)
        
        try:
            process_file(readfilepath, savefilepath, outdir)
        except Exception as e:
            print("\t!FAIL: %s." % str(e))
            print e
            fail_count += 1
        else:
            print("\tSuccess, saved as '%s'." % savename)
            success_count += 1
            
        print("") # empty line
            
    print("") # empty line
    print("Total number of files processed: %d; success: %d; fail: %d." % (
        success_count+fail_count, success_count, fail_count))
      
    
def process_file(infile, outfile, outdir):
    """ Takes file infile and creates plot image outfile. """
    
    # getting data for the plot
    with open(infile) as f_data:
        content = f_data.readlines()

    x_data = []
    y_data = []
    started_read = False
    for line in reversed(content):
        data = re.split(r"\s+", line)
        
        if not data[0].isdigit():
            if not started_read:
                continue
            else:
                break
        started_read = True
        
        x_data.append(float(data[1]))
        y_data.append(float(data[2]))


    x_data = tuple(reversed(x_data))
    y_data = tuple(reversed(y_data))
    print outfile

    # drawing plot
    lorentz.background_substraction(x_data,y_data,outfile,infile)

    # saving plot
    #plt.savefig(outfile, bbox_inches='tight', transparent=False)

if __name__ == "__main__":
    
    inputdir = "indir"
    outputdir = "outdir"

    # reading command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print("test.py -i <inputfile> -o <outputfile>")
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == "-h":
            print("txt_images.py -i <inputdir> -o <outputdir>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputdir = arg
        elif opt in ("-o", "--ofile"):
            outputdir = arg
    
    if inputdir is None:
        inputdir = os.getcwd()
        print inputdir

    if outputdir is None:
        outputdir = inputdir
    res = open(outputdir+'/results.txt','w')   
    res.close()  
    process_dir(inputdir, outputdir)
