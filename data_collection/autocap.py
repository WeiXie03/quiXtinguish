import cv2, numpy as np
import socket, os, sys, pickle
import recvid_multipi as stream



if __name__ == "__main__":
    left = stream.Cam(5400, 'left')
    right = stream.Cam(5800, 'right')
