import numpy as np
import cv2
from stopwatch import stopwatch


def morse_parser(decoder):
    cap = cv2.VideoCapture(0)

    lightTimer = stopwatch()
    pauseTimer = stopwatch()


    lightArray = []
    bX, bY, bW, bH = 230, 360, 220 + 230, 360 - 180
    lightFound = False
    newline = False
    while 1:
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # filtering to remove  grains
        kernel = np.ones((5, 5), np.float32) / 25
        dst = cv2.filter2D(hsv, -1, kernel)

        # lower and upper hsv values
        lower = np.array([0, 0, 250])
        upper = np.array([180, 10, 255])

        mask = cv2.inRange(dst, lower, upper)  # generate mask based on values
        res = cv2.bitwise_and(frame, frame, mask=mask)  # overlay mask ontop of video
        blur = cv2.medianBlur(res, 5)

        # retrive edges of detection
        edges = cv2.Canny(blur, 100, 200)

        cv2.rectangle(frame, (bX, bY), (bW, bH), (0, 255, 0), 2)

         # get contours from edges
        im2, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            # print("LIGHT DETECTED")
            c = max(contours, key=cv2.contourArea)

            (x, y), radius = cv2.minEnclosingCircle(c)
            center = (int(x), int(y))
            radius = int(radius)
            if bW > x > bX:
                if bH < y < bY:
                    lightFound = True
                    cv2.circle(frame, center, radius, (255, 0, 0), 4)
            else:
                lightFound = False

            # cv2.drawContours(frame, c, -1, (255, 0, 0), 3)

        else:
            lightFound = False

        if lightFound:
            newline = True
            if pauseTimer.is_running():
                pauseTimer.stop()

            if not lightTimer.is_running():
                lightTimer.start()
        else:
            if lightTimer.is_running():
                lightTimer.stop()
                lightArray.append(round(lightTimer.get_elapsed(), 2))
            else:
                if not pauseTimer.is_running():
                    pauseTimer.start()
                if decoder.pauseRange[0] <= pauseTimer.get_elapsed() < decoder.pauseRange[1]:
                        if len(lightArray) > 0:
                            # send request to morse

                            morse = decoder.to_morse_string(lightArray)
                            print(decoder.to_alpha(morse), end="", flush=True)
                            lightArray.clear()

                if pauseTimer.get_elapsed() >= decoder.space:
                    if newline:
                        print("\n")
                        newline = False
        # PROGRESSION:

        cv2.imshow("edges", edges)
        cv2.imshow('frame', frame)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    print(lightArray)
    cv2.destroyAllWindows()
    cap.release()