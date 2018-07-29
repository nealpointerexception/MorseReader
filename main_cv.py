import numpy as np
import cv2, threading
from stopwatch import stopwatch


def morse_parser(decoder):
    cap = cv2.VideoCapture(0)

    light_timer = stopwatch()
    pause_timer = stopwatch()

    light_array = []
    b_x, b_y, b_w, b_h = 230, 360, 220 + 230, 360 - 180
    light_found = False
    newline = False

    def run_decoder(arr=[]):
        morse = decoder.to_morse_string(arr)
        print(decoder.to_alpha(morse), end="", flush=True)

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

        # retrieve edges of detection
        edges = cv2.Canny(blur, 100, 200)

        cv2.rectangle(frame, (b_x, b_y), (b_w, b_h), (0, 255, 0), 2)

        # get contours from edges
        im2, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            # print("LIGHT DETECTED")
            c = max(contours, key=cv2.contourArea)

            (x, y), radius = cv2.minEnclosingCircle(c)
            center = (int(x), int(y))
            radius = int(radius)
            if b_w > x > b_x:
                if b_h < y < b_y:
                    light_found = True
                    # cv2.drawContours(frame, c, -1, (255, 0, 0), 3)
                    cv2.circle(frame, center, radius, (255, 0, 0), 4)
            else:
                light_found = False

        else:
            light_found = False

        if light_found:
            newline = True
            if pause_timer.is_running():
                pause_timer.stop()

            if not light_timer.is_running():
                light_timer.start()
        else:
            if light_timer.is_running():
                light_timer.stop()
                light_array.append(round(light_timer.get_elapsed(), 2))
            else:
                if not pause_timer.is_running():
                    pause_timer.start()
                if decoder.get_pause_range()[0] <= pause_timer.get_elapsed() < decoder.get_pause_range()[1]:
                    run_decoder(light_array)
                    light_array.clear()

                if pause_timer.get_elapsed() >= decoder.get_space():
                    if newline:
                        print("\n")
                        newline = False
        # PROGRESSION:

        cv2.imshow("edges", edges)
        cv2.imshow('frame', frame)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    print(light_array)
    cv2.destroyAllWindows()
    cap.release()
