import numpy as np
import cv2
from stopwatch import stopwatch
from morse import morse

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)

    lightTimer = stopwatch()
    pauseTimer = stopwatch()

    spaceBetweenLetters = 0.29
    spaceBetweenWords = 1;

    calibLightArray = []
    morsey = morse()

    while True:
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
                calibLightArray.append(round(pauseTimer.get_elapsed(), 2))
                pauseTimer.stop()

            if not lightTimer.is_running():
                lightTimer.start()

        else:
            if lightTimer.is_running():
                lightTimer.stop()
                calibLightArray.append(round(lightTimer.get_elapsed(), 2))
            else:
                if not pauseTimer.is_running():
                    pauseTimer.start()
                else:
                    if(pauseTimer.get_elapsed() >= 6 and len(calibLightArray) > 0):
                        print("Calibration Complete")
                        #print(".(pause).(pause).(pause).(pause)+(space) -(pause)-(pause)-")
                        del(calibLightArray[0])
                        print(calibLightArray)
                        morsey.calibrate(calibLightArray)
                        break









        # PROGRESSION:

        cv2.imshow("edges", edges)
        cv2.imshow('frame', frame)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break





    cv2.destroyAllWindows()
    cap.release()