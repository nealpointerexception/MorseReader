import numpy as np
import cv2
from stopwatch import stopwatch
from morse import morse
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    lightTimer = stopwatch()
    pauseTimer = stopwatch()

    conv = morse()

    lightArray = []
    while(1):
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #filtering to remove  grains
        kernel = np.ones((5, 5), np.float32) / 25
        dst = cv2.filter2D(hsv, -1, kernel)

        # lower and upper hsv values
        lower = np.array([0, 0, 250])
        upper = np.array([180, 10, 255])

        mask = cv2.inRange(dst, lower, upper) # generate mask based on values
        res = cv2.bitwise_and(frame, frame, mask=mask) #overlay mask ontop of video
        blur = cv2.medianBlur(res, 5)

        #retrive edges of detection
        edges = cv2.Canny(blur, 100, 200)

        #get contours from edges
        im2, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            #print("LIGHT DETECTED")
            c = max(contours, key=cv2.contourArea)

            (x, y), radius = cv2.minEnclosingCircle(c)
            center = (int(x), int(y))
            radius = int(radius)

            cv2.circle(frame, center, radius, (0, 255, 0), 2)
            #cv2.drawContours(frame, c, -1, (255, 0, 0), 3)
            if pauseTimer.is_running():
                pauseTimer.stop()

            if not lightTimer.is_running():
                lightTimer.start()

        else:
            if lightTimer.is_running():
                lightTimer.stop()
                lightArray.append(lightTimer.get_elapsed())
            else:
                if not pauseTimer.is_running():
                    pauseTimer.startTime()
                else:
                    if(pauseTimer.get_elapsed() >= 3):
                        if(len(lightArray) > 0):
                            # send request to morse
                            print("MORSE-ING TIME")
                            lightArray.clear()









        # PROGRESSION:
        cv2.imshow('frame', frame)
        # cv2.imshow('hsv', hsv)
        # cv2.imshow('mask', mask)
        # cv2.imshow('res', res)
        # cv2.imshow('blur', blur)
        cv2.imshow("edges", edges)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break



    print(lightArray)
    rounded = []
    for t in lightArray:
        rounded.append(round(t))
    print(rounded)
    cv2.destroyAllWindows()
    cap.release()