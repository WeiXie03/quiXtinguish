import numpy, math
import os, pickle, sys
import matplotlib.pyplot as plt
from scipy import optimize
from mpl_toolkits.mplot3d import Axes3D
import calcDepth as dep
from matplotlib import cm

def calc_height(ydiff, depth, focl):
    #used similar triangles
    return numpy.multiply(depth*100, ydiff)/focl

def rmse(predictions, real):
    return numpy.sqrt(((predictions - real) ** 2).mean())

if __name__ == "__main__":
    DATA_DIR = sys.argv[1]
    CALIB_DIR = sys.argv[2]

    #NOTE: EVERYTHING's in cm
    BASELINE = 21.85
    print('baseline = {} centimeters'.format(BASELINE))
    CAM_HEIGHT = 14.4 #cm
    IMG_HEIGHT = 480
    FOCLX = dep.load_foclx(CALIB_DIR)

    metadata_path = os.path.join(DATA_DIR, 'metadata.dat')
    with open(metadata_path, 'rb') as metadataf:
        metadata = pickle.load(metadataf)

    heights = []
    ydiffs = []
    depths = []
    for pairnum in range(478):
    #for pairnum in range(len(metadata.keys())):
        #print('pair', pairnum)
        #convert to meters
        height = metadata[pairnum]['fire height from ground'] - CAM_HEIGHT
        heights.append(height)

        depth = metadata[pairnum]['real depth']
        depths.append(depth)

        ly = metadata[pairnum]['left']['coords'][1]
        ry = metadata[pairnum]['right']['coords'][1]
        #average y coords of left and right
        ycoord = (ly+ry)/2.0

        ydiffs.append(IMG_HEIGHT/2-ycoord)

    #experimental
    ydiffs = numpy.asarray(ydiffs).astype(numpy.float)
    depths = numpy.asarray(depths).astype(numpy.float)
    heights = numpy.asarray(heights).astype(numpy.float)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(ydiffs, depths, zs=heights, zdir='z', c='m', label='experimental')

    #theoretical
    ys = numpy.linspace(1, 239, 239)
    estdepths = numpy.linspace(2, 9, 9-1)

    Ys, Deps = numpy.meshgrid(ys, estdepths)
    Z = numpy.asarray(calc_height(Ys, Deps, FOCLX))
    ax.contour3D(Ys, Deps, Z, numpy.linspace(1,60,30), cmap=cm.jet)

    #axes labels
    ax.set_xlabel('y Coordinates from Horizontal Image Halfline(px)')
    ax.set_ylabel('Depth(m)')
    ax.set_zlabel('Height(cm)')
    #ax.legend()
    ax.set_title('Height of Fire Estimation Accuracy')

    plt.show()

    #calculate root mean squared error
    print('real', heights.shape, 'predictions', Z.shape)
    print(Z)
    print('root mean squared error for height prediction =', rmse(calc_height(ydiffs, depths, FOCLX), heights))
