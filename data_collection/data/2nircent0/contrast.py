import cv2, numpy as np
import os, sys, pickle

'''
def contrastify(image):
    #histogram equalization
    hist, bins = np.histogram(image.flatten(),256,[0,256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max()/ cdf.max()
    cdf_m = np.ma.masked_equal(cdf,0)
    cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
    cdf = np.ma.filled(cdf_m,0).astype('uint8')
    image = cdf[image]

    return image
'''
def contrastify(image):
    #convert to LAB colour space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    lab_planes = cv2.split(lab)

    #apply CLAHE algorithm
    clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(80,60))
    lab_planes[0] = clahe.apply(lab_planes[0])

    lab = cv2.merge(lab_planes)
    bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    return bgr

def load_meta(metaf_path):
    with open(metaf_path, 'rb') as metaf:
        metadata = pickle.load(metaf)
    return metadata

if __name__ == "__main__":
    metaf_path = os.path.join(sys.argv[1])
    metadata = load_meta(metaf_path)

    for pairind in range(len(metadata.keys())):
        for src in 'left', 'right':
            #load each image
            impath = os.path.join(metadata[pairind][src]['img_path'])
            print(impath)
            img = cv2.imread(impath)
            #increase contrast
            img = contrastify(img)
            #save new image, ENSURE BACKUP CREATED
            print('writing image', pairind, src)
            cv2.imwrite(impath, img)
