import cv2, numpy, sys, os

cur, prev = cv2.imread(sys.argv[2]), cv2.imread(sys.argv[1])

#show the difference in consecutive frames for each camera
diff = numpy.abs(cur.astype(numpy.int8) - prev.astype(numpy.int8)).astype(numpy.uint8)
print(numpy.max(diff))

key_hit = None
while(key_hit != ord('q')):
    cv2.imshow('diff', numpy.hstack(((diff*(254/numpy.max(diff))).astype(numpy.uint8), cur, prev)))
    key_hit = cv2.waitKey(1)

    if key_hit == ord('w'):
        cv2.imwrite(os.path.join('/home/wei/Pictures/flamediff_left.jpg'), (diff*(254/numpy.max(diff))).astype(numpy.uint8))
        cv2.imwrite(os.path.join('/home/wei/Pictures/{}'.format(sys.argv[2])), cur)
        cv2.imwrite(os.path.join('/home/wei/Pictures/{}'.format(sys.argv[1])), prev)
        print('saved')
