import cv2
import numpy as np
import os, sys, pickle
import csv
import matplotlib.pyplot as plt

#takes 2 coords as tuples in the form (x, y), baseline in the units desired, focl in pixels
def calcDepth(baseline, focl, lcoords, rcoords, rldepth):
    #disparity = left x - right x
    #objects always appear farther right from left perspective, right is positive horiz direction in OpenCV GUI; ALWAYS subtract right x from left x
    #refer to https://docs.opencv.org/3.4.5/dc/dbb/tutorial_py_calibration.html for calculating depth
    disp = (lcoords[0] - rcoords[0])

    #est_depth = (baseline*focl)/disp

    rlfocl = (disp*rldepth)/baseline
    print('rldepth ', rldepth)
    #avg_est_focl=602.4174387053763
    avg_est_focl=861.19 - 0.4311654*rldepth
    disp = (lcoords[0] - rcoords[0])-5
    print('rlfocl ', rlfocl, ', old calc depth ', (baseline*avg_est_focl)/disp)
    disp = (lcoords[0] - rcoords[0])
    print('rlfocl ', rlfocl, ', new calc depth ', (baseline*avg_est_focl)/disp)

    #print('rl focal length', (disp*215)/baseline) #for img 8

    #return(est_depth)
    return rlfocl,(baseline*avg_est_focl)/disp

if __name__ == "__main__":
    DATA_DIR = sys.argv[1]

    metadata_path = os.path.join(DATA_DIR, 'metadata.dat')
    #load metadata
    if os.path.isfile(metadata_path):
        with open(metadata_path, 'rb') as metadataf:
            metadata = pickle.load(metadataf)
    else:
        print('metadata not found, aborting')
        sys.exit()

    '''
    while True:
        pairNum = input('Enter the number of the stereo image pair concerned or q to exit.\t')
        if pairNum == 'q':
            break
        else:
            pairNum = int(pairNum)
            paird = metadata[pairNum]
        print(paird)
    '''
    sum = 0
    count = 0
    xs = []
    ys = []
    ys1 = []
    for pairNum in range(len(metadata.keys())):
        paird = metadata[pairNum]
        #just assuming one fire for now
        lcoords = paird['left']['coords'][0]
        rcoords = paird['right']['coords'][0]
        nircoords
        print('left ', lcoords, '\tright ', rcoords)

        #baseline = float(input('How far are the cameras\' lens centers? Answer in the units you would like the depth in.\t'))
        #baseline = 26.4 #cm
        baseline = 35.9 #cm

        #CALIB_PATH = "./calibration/camMtx.npy"
        #if os.path.isfile(CALIB_PATH):
        #    calib = numpy.load(CALIB_PATH)
        #    print(calib)
        #focal length y from stereo calibration
        #focl = calib[0][0]
        #focl = 1237.878787878788 #calculated from image 8 of test/, see calcDepth()
        focl = 602.4174387053763 #calculated

        if metadata[pairNum]['fire height'] > 50:
            print(pairNum,metadata[pairNum]['fire height'])

            rldepth = paird['real depth']

            xs.append(rldepth)
            rlfocl, est_depth = calcDepth(baseline, focl, lcoords, rcoords, rldepth)
            ys.append(rlfocl)
            ys1.append(est_depth)
            #paird['estimated depth'] = est_depth
            #metadata[pairNum] = paird
            sum += rlfocl#calcDepth(baseline, focl, lcoords, rcoords, rldepth)
            print('focal length = ', rlfocl, '\n')
            count +=1

    print('average focl is ', sum/count)
    plt.scatter(xs, ys1)
    plt.plot([0,1000],[0,1000])
    plt.xlabel("Estimated Depth [cm]")
    plt.ylabel("Real Depth [cm]")
    plt.title("Accuracy of Depth Estimation")
    plt.show()
    xs = np.asarray(xs)
    ys = np.asarray(ys)
    m,b = np.polyfit(xs, ys, 1)
    plt.scatter(xs, ys)
    plt.plot(xs, xs*m+b)
    print(m, b)
    plt.show()

    '''
    print(metadata)
    dec = input('Would you like to write to metadata?[y/n]: ')
    if dec == 'y':
        with open(metadata_path, 'wb') as metadataf:
            pickle.dump(metadata, metadataf)
    else:
        print('aborting')
    '''
