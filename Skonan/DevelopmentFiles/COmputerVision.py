import cv2
import numpy as np


def onmouse(k,x,y,s,p):
    if k==1:   # left mouse, print pixel at x,y
        print ([x,y])

if __name__ == '__main__':

    img = cv2.imread('FRC.jpg')

    length1,width1,channels = img.shape
    img = cv2.GaussianBlur(img, (5, 5), 0)


    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


    lower_green = np.array([75, 200, 170])
    upper_green = np.array([90, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_and(hsv, hsv, mask=mask)

    h,s,v = cv2.split(res)


    im2,contours,hierarchy = cv2.findContours(s,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    #print("Contours: %d" % contours.size())
    #print("Hierarchy: %d" % hierarchy.size())

    cv2.drawContours(img,contours[0], -1, (0, 0, 255), 3)


    cnt = contours[0]
    perimeter = cv2.arcLength(cnt, True)


    M = cv2.moments(cnt)

    cx = int(M['m10'] / M['m00'])#Center of MASS Coordinates
    cy = int(M['m01'] / M['m00'])

    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(img, [box], 0, (255, 0, 0), 2)
    cv2.circle(img, (cx, cy), 7, (0, 0, 255), -1)

    print('The len and width of the fitted rectangle are (in pixels): %s,%s' % (int(rect[1][1]), int(rect[1][0])))
    print('Center of Mass is Approx at Location: %s,%s' % (cx,cy))

    if(cx < length1/2):
        print('Move to the right')
    else:
        print('Move to the left')

    cv2.namedWindow("Image w Contours")
    cv2.setMouseCallback("Image w Contours", onmouse)
    cv2.imshow('Image w Contours', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



    #im2, contours, hierarchy = cv2.findContours(threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #cv2.drawContours(threshed, contours, -1, (0, 255, 0), 3)

    



    """
lower_green = np.array([75,200,200])
upper_green = np.array([85,255,255])
mask = cv2.inRange(hsv, lower_green, upper_green)
res = cv2.bitwise_and(img,img,mask=mask)
cv2.imshow('orig',img)
cv2.imshow('fff',res)

cv2.waitKey(0)
cv2.destroyAllWindows()

"""