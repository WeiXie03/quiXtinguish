import numpy, math
import os, pickle, sys
import matplotlib.pyplot as plt
from scipy import optimize
from mpl_toolkits.mplot3d import Axes3D

def calc_height(dist, ycoord, imgh, camh, focl):
    #used similar triangles
    return ((dist*((imgh/2)-ycoord))/focl)+camh

if __name__ == "__main__":
    DATA_DIR = sys.argv[1]
    print('hm')
    CALIB_DIR = numpy.load(os.path.join(sys.argv[2]))
    print('hm1')

    BASELINE = 21.85/10**2
    print('baseline = {} meters'.format(BASELINE))
    CAM_HEIGHT = 14.4/10**2 #meters
    IMG_HEIGHT = 480

    metadata_path = os.path.join(DATA_DIR, 'metadata.dat')
    print('hm2')
    with open(metadata_path, 'rb') as metadataf:
        metadata = pickle.load(metadataf)
    print('hm3')

    heights = []
    ydiffs = []
    depths = []
    for tripnum in range(len(metadata.keys())):
        print(tripnum)
        height = metadata[tripnum]['fire height from ground']/10.0**2 - CAM_HEIGHT
        heights.append(height)

        depth = metadata[tripnum]['real depth']
        depths.append(depth)

        ycoord = metadata[tripnum]['NoIR']['coords'][1]
        ydiffs.append(IMG_HEIGHT/2-ycoord)
        print(IMG_HEIGHT/2-ycoord)

    ydiffs = numpy.asarray(ydiffs).astype(numpy.float)
    depths = numpy.asarray(depths).astype(numpy.float)
    heights = numpy.asarray(heights).astype(numpy.float)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(ydiffs, depths, zs=heights, zdir='z', c='r')

    plt.show()
