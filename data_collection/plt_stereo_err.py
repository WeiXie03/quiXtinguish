import numpy, math
import os, pickle, sys
import matplotlib.pyplot as plt
from scipy import optimize

def calc_depth(disps, focl, bias):
    return numpy.reciprocal(disps+bias) * (39.5/10**2)*focl

if __name__ == "__main__":
    DATA_DIR = sys.argv[1]
    CALIB_MTX = numpy.load(os.path.join(sys.argv[2]))

    BASELINE = 39.5/10**2
    print('baseline = {} meters'.format(BASELINE))
    CAM_HEIGHT = 17.1/10**2 #meters

    metadata_path = os.path.join(DATA_DIR, 'metadata.dat2')
    with open(metadata_path, 'rb') as metadataf:
        metadata = pickle.load(metadataf)

    errs = []
    depths = []
    dists = []
    disps = []
    for tripnum in range(len(metadata.keys())):
        depth = metadata[tripnum]['real depth']
        depths.append(depth)

        height = metadata[tripnum]['fire height from ground']/10**2 - CAM_HEIGHT
        #pythag: distance = sqrt(depth^2 + (fire height - camera height)^2)
        dist = (depth**2+height**2)**0.5
        dists.append(dist)

        disp = abs(metadata[tripnum]['left']['coords'][0]-metadata[tripnum]['right']['coords'][0])
        disps.append(disp)

        estdepth = (BASELINE*CALIB_MTX[0][0])/disp

        err = math.fabs(estdepth - depth)
        errs.append(err)

    disps = numpy.asarray(disps).astype(numpy.float)
    recip_disps = numpy.reciprocal(disps)

    print('erros in cm', errs, ', distances', depths)
    #plt.plot(recip_disps, dists, 'bo')
    plt.plot(disps, depths, 'bo', label='Experimental')

    plt.xlabel('Disparity(pixels)')
    plt.ylabel('Depth(meters)')

    #fit straight line
    xs = numpy.linspace(disps[0], disps[-1], len(depths))
    m, b = numpy.polyfit(recip_disps, depths, 1)
    plt.plot(xs, m*numpy.reciprocal(xs)+b, 'r-', label='Theoretical')

    plt.title('Depth of Fire vs Disparity of Corresponding Points on Stereo Images Representing Fire')
    plt.legend()

    '''
    #fit a reciprocal function
    xs = numpy.linspace(disps[0], disps[-1], len(depths))
    #print(xs, depths)
    #print(CALIB_MTX[0][0]*0.7)
    popt, pcov = optimize.curve_fit(calc_depth, disps, depths, bounds=(CALIB_MTX[0][0]*0.5, CALIB_MTX[0][0]*0.8))
    #print(popt)
    plt.plot(xs, calc_depth(xs, *popt), 'r-')
    '''

    plt.show()
