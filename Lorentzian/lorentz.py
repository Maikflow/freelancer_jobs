########################IMPORTING REQUIRED MODULES ######################
import re
import numpy
import pylab
from scipy.optimize import leastsq # Levenberg-Marquadt Algorithm #
from os import listdir
import os
from pylab import grid
#########################################################################
####################0####### DEFINING FUNCTIONS ##########################
def find_nearest(array,value):
    idx = (numpy.abs(array-value)).argmin()
    return (idx,array[idx])

def lorentzian(x,p):
    numerator =  (p[0]**2 )
    denominator = ( x - (p[1]) )**2 + p[0]**2
    y = p[2]*(numerator/denominator)
    return y

def residuals(p,y,x):
    err = y - lorentzian(x,p)
    return err

#########################################################################
######################## BACKGROUND SUBTRACTION #########################

def background_substraction(x_data,y_data,outfile,infile):
    """Substracts the background and starts the fitting"""
    x = numpy.array(x_data)
    y = numpy.array(y_data)

    #find the peak 
    peak = max(y)
    peak_index = numpy.where(y==peak)[0][0]

    #Find -3db xvalues left and right of the peak
    right_index = find_nearest(y[peak_index:],peak-3)[0] 
    left_index = find_nearest(y[peak_index::-1],peak-2)[0] 
    db_left = x[peak_index-left_index]
    db_right = x[peak_index+right_index]
   # print x[peak_index-left_index:peak_index+right_index]
   # print y[peak_index-left_index:peak_index+right_index]
    print db_left, 'db right', db_right

    with open('outdir/results.txt','a') as f:
        results = '''
        file = {}
        {} {} {} {} {}
        '''.format(infile,peak,db_left,peak-3,db_right,peak-3)

        f.write(results)

    #Find the peak center (x where y is max)
    center = x[peak_index]

    #Calculate the half-width at half maximum
    hwhm = abs(.25/(3.1416*peak))
    print hwhm, 'center', center

    #Parameters
    p = [hwhm,center,peak]  # [hwhm, peak center, intensity] #

    # defining the 'background' part of the spectrum #
    ind_bg_low = (x > min(x)) & (x < db_left)
    ind_bg_high = (x > db_right) & (x < max(x))

    x_bg = numpy.concatenate((x[ind_bg_low],x[ind_bg_high]))
    y_bg = numpy.concatenate((y[ind_bg_low],y[ind_bg_high]))
    #pylab.plot(x_bg,y_bg)

    # fitting the background to a line # 
    m, c = numpy.polyfit(x_bg, y_bg, 1)

    # removing fitted background # 
    background = m*x + c
    y_bg_corr = y - background
    #pylab.plot(x,y_bg_corr)
    fit_data(y_bg_corr,x,p,outfile)

#########################################################################
############################# FITTING DATA ## ###########################
def fit_data(y_bg_corr,x,p,outfile):
    # optimization # 
    pbest = leastsq(residuals,p,args=(y_bg_corr,x),full_output=1)
    print (pbest)
    best_parameters = pbest[0]
    print best_parameters

    # fit to data #
    fit = lorentzian(x,best_parameters)
    plot_lorentzian(y_bg_corr,x,fit,outfile)

#########################################################################
############################## PLOTTING #################################
def plot_lorentzian(y_bg_corr,x,fit,outfile):
    grid(True)
    peak = max(y_bg_corr)
    peak_index = numpy.where(y_bg_corr==peak)[0][0]
    
    #offset to eliminate background (userdefines)
    offsetl = -45
    offsetr = 95
    #Find -3db xvalues left and right of the peak
    right_index = find_nearest(y_bg_corr[peak_index:],peak-3)[0] 
    left_index = find_nearest(y_bg_corr[peak_index::-1],peak-3)[0] 
    
    if offsetl or offsetr:
         x = x[peak_index-left_index+offsetl:peak_index+right_index+offsetr]
         y_bg_corr = y_bg_corr[peak_index-left_index+offsetl:peak_index+right_index+offsetr]
         fit = fit[peak_index-left_index+offsetl:peak_index+right_index+offsetr]

    pylab.plot(x ,y_bg_corr,'wo')
    pylab.plot(x ,fit,'r-',lw=2)
    pylab.xlabel('GHz', fontsize=18)
    pylab.ylabel('DB', fontsize=18)
    pylab.savefig(outfile)    

    #Save lorentzian fit files to results.txt
    #with open('outdir/results.txt','a+') as f:
    #    f.write('\nLorentzian Fit:\n')
    #    for i,value in enumerate(x):
    #        f.write(str(value)+'    '+str(fit[i])+'\n')
        
    pylab.show()
    

#########################################################################
############################# LOADING DATA ##############################
if __name__ == "__main__":
    indir = os.getcwd()
    for fname in listdir(indir):
        if fname.endswith('.txt'):
            readfilepath = os.path.join(indir, fname)

    # getting data for the plot
    with open(readfilepath, 'r') as f_data:
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
    background_substraction(x_data,y_data)
