import numpy as np
import cv2


def onmouse(k,x,y,s,p):
    global hsv
    if k==1:   # left mouse, print pixel at x,y
        print(hsv[y,x])


if __name__ == '__main__':

    widthMin = 100
    heightMin = 0
    widthmax = 10000
    heightmax = 10000

    cap = cv2.VideoCapture(0)
    print('press x to exit')
    while(True):
        # Capture frame-by-frame
        ret, img = cap.read()

        length1, width1, channels = img.shape
        img = cv2.GaussianBlur(img, (5, 5), 0)

        hsv = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2HSV)


        #lower_green = np.array([75, 200, 170])
        lower_green = np.array([75, 40, 170])

        upper_green = np.array([90, 150, 255])

        mask = cv2.inRange(hsv, lower_green, upper_green)
        res = cv2.bitwise_and(hsv, hsv, mask=mask)

        h, s, v = cv2.split(res)

        im2, contours, hierarchy = cv2.findContours(h, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        # print("Contours: %d" % contours.size())
        # print("Hierarchy: %d" % hierarchy.size())


        if(len(contours ) != 0):

            cv2.drawContours(img, contours[0], -1, (0, 0, 255), 3)


            cnt = contours[0]
            perimeter = cv2.arcLength(cnt, True)


            M = cv2.moments(cnt)

            cx= 0
            cy = 0

            if(M['m00'] != 0):
                cx = int(M['m10'] / M['m00'])  # Center of MASS Coordinates
                cy = int(M['m01'] / M['m00'])

            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(img, [box], 0, (255, 0, 0), 2)
            cv2.circle(img, (cx, cy), 7, (0, 0, 255), -1)

            cv2.line(img,(int(width1/2),int(length1/2)),(cx, cy),(255, 0, 0),2)
            #print('The len and width of the fitted rectangle are (in pixels): %s,%s' % (int(rect[1][1]), int(rect[1][0])))
            #print('Center of Mass is Approx at Location: %s,%s' % (cx, cy))

            #if (cx < length1 / 2):
                #print('Move to the right')
            #else:
                #print('Move to the left')

        cv2.namedWindow("Image w Contours")
        cv2.setMouseCallback("Image w Contours", onmouse)
        cv2.imshow('Image w Contours', img)

        

        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
