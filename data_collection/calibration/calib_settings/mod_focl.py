import os, sys
import numpy

def load_mtx(calib_path):
    '''
    obtains a camera matrix from calib_path and returns it
    '''
    cam_mtx = numpy.load(os.path.join(calib_path))

def tune_foclx(calibf_path, rlfoclx):
    '''
    copies and corrects a camera matrix, returns whole calibrated settings data
    '''
    calib_data = numpy.load(calibf_path)
    calib_data[0][0][0] = rlfoclx
    print('real focal = {}'.format(rlfoclx))
    return calib_data

if __name__ == "__main__":
    print('enter calibration settings directory as command line arg')
    CALIB_DIR = sys.argv[1]

    rlfoclx = float(input('enter the real focal length in pixels: '))

    for side in 'left', 'right':
        calibf_path = os.path.join(CALIB_DIR, 'calib_settings_{}.npy'.format(side))

        #get correct copy of calibrated settings
        corr_calib = tune_foclx(calibf_path, rlfoclx)
        #save em
        numpy.save(calibf_path, corr_calib)
