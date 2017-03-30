import time
import argparse

import cv2
import numpy as np
from imutils.video import VideoStream

ap = argparse.ArgumentParser()
ap.add_argument('-p', '--picamera', type=int, default=-1,
                help='whether or not the Raspberry Pi camera should be used')
args = vars(ap.parse_args())

vs = VideoStream(usePiCamera=args['picamera'] > 0).start()
print('Acquired camera, pausing for 2 seconds')
time.sleep(2.0)

while True:
    frame = vs.read()

    height = np.size(frame, 0)
    width = np.size(frame, 1)

    region = cv2.cvtColor(frame[(height * 5 / 6):height, 10:(width - 10)], cv2.COLOR_BGR2GRAY)
    region = cv2.GaussianBlur(region, (21, 21), 0)
    th, region = cv2.threshold(region, 100, 255, cv2.THRESH_BINARY_INV)
    contoured, contours, heirarchy = cv2.findContours(region, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    display = frame.copy()
    display_region = display[(height * 5 / 6):height, 10:(width - 10)]

    for contour in contours:
        m = cv2.moments(contour)
        if m['m00'] > 100:
            cx = int(m['m10'] / m['m00'])
            cy = int(m['m01'] / m['m00'])
            cv2.circle(display_region, (cx, cy), 10, (0, 0, 255), -1)

    cv2.drawContours(display_region, contours, -1, (0, 255, 0), 1)
    cv2.imshow('Source', display)
    cv2.imshow('Frame', region)

    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()
