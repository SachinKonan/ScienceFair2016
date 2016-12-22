import numpy as np
import cv2


def onmouse(k,x,y,s,p):
    global hsv
    if k==1:   # left mouse, print pixel at x,y
        print(hsv[y,x])


if __name__ == '__main__':

    counter = 0
    cap = cv2.VideoCapture(1)
    print('press x to exit')
    while(True):

        ret,img = cap.read()
        cv2.imshow('Data',img)

        print(img.shape)
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break


    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()