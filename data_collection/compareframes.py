import cv2, numpy, sys

cur, prev = cv2.imread(sys.argv[2]), cv2.imread(sys.argv[1])

#show the difference in consecutive frames for each camera
diff = numpy.abs(cur.astype(numpy.int8) - prev.astype(numpy.int8)).astype(numpy.uint8)
print(numpy.max(diff))
cv2.imshow('diff', numpy.hstack(((diff*(254/numpy.max(diff))).astype(numpy.uint8), cur, prev)))
cv2.waitKey()
