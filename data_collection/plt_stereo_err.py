import numpy, math
import os, pickle, sys
import matplotlib.pyplot as plt
from scipy import optimize

def load_foclx(calib_path):
    '''
    Averages x focal length of left and right cameras stored in calibrated settings
    '''
    lcalib = numpy.load(os.path.join(calib_path, 'calib_settings_left.npy'))
    rcalib = numpy.load(os.path.join(calib_path, 'calib_settings_right.npy'))

    foclx = (lcalib[0][0][0] + rcalib[0][0][0])/2
    return foclx

def calc_depth(disps, focl, bias):
    return numpy.reciprocal(disps+bias) * (21.85/100)*focl

if __name__ == "__main__":
    DATA_DIR = sys.argv[1]
    CALIB_DIR = sys.argv[2]

    BASELINE = 21.85/100
    print('baseline = {} meters'.format(BASELINE))
    CAM_HEIGHT = 14.0/100 #meters
    FOCLX = load_foclx(CALIB_DIR)

    metadata_path = os.path.join(DATA_DIR, 'metadata.dat')
    with open(metadata_path, 'rb') as metadataf:
        metadata = pickle.load(metadataf)

    errs = []
    depths = []
    disps = []
    for pairnum in range(len(metadata.keys())):
        try:
            depth = metadata[pairnum]['real depth']

            height = metadata[pairnum]['fire height from ground']/10**2 - CAM_HEIGHT

            disp = metadata[pairnum]['left']['coords'][0]-metadata[pairnum]['right']['coords'][0]

            #err = math.fabs(estdepth - depth)
        except KeyError:
            print('potentially no experimental depth and/or height data for set {}, skipping'.format(pairnum))

        except TypeError:
            print('potentially no fires in image(s)')
            continue
        else:
            depths.append(depth)

            disps.append(disp)

            estdepth = (BASELINE*FOCLX)/disp
            print(pairnum, ':', estdepth, 'meters')

            #errs.append(err)

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
    print('f(x) = {}x + {}'.format(m, b))
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
