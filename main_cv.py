import numpy as np
import cv2, threading
from stopwatch import stopwatch


def morse_parser(decoder):
    # get capture from default camera
    cap = cv2.VideoCapture(0)

    # create timers fro timing pauses and lights
    light_timer = stopwatch()
    pause_timer = stopwatch()

    light_array = []
    b_x, b_y, b_w, b_h = 230, 360, 220 + 230, 360 - 180 # bounding box coords
    light_found = False
    newline = False

    def run_decoder(arr=[]):
        morse = decoder.to_morse_string(arr)
        print(decoder.to_alpha(morse), end="", flush=True)

    while 1:
        ret, frame = cap.read() #get frame from camera
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # convert frame capture to HSV values

        # filtering to remove  grains
        kernel = np.ones((5, 5), np.float32) / 25
        dst = cv2.filter2D(hsv, -1, kernel) # stage 2 of filtering (this is what you modify after frame)

        # lower and upper hsv values -- gets white values
        lower = np.array([0, 0, 250])
        upper = np.array([180, 10, 255])


        mask = cv2.inRange(dst, lower, upper)  # generate mask based on values on the dst
        res = cv2.bitwise_and(frame, frame, mask=mask)  # overlay mask on top of video
        blur = cv2.medianBlur(res, 5) # apply blur to soften mask

        # retrieve edges of detection
        edges = cv2.Canny(blur, 100, 200)

        cv2.rectangle(frame, (b_x, b_y), (b_w, b_h), (0, 255, 0), 2) # draw bounding box rectangle

        # get contours from edges -- just let opencv do its thing
        im2, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            # print("LIGHT DETECTED")
            c = max(contours, key=cv2.contourArea)  # get the largest area contour

            (x, y), radius = cv2.minEnclosingCircle(c)  # get an enclosing circle for the contour

            center = (int(x), int(y)) # get center of circle (for coords)
            radius = int(radius)

            # logic to check if the circle is inside the bounding box
            if b_w > x > b_x:
                if b_h < y < b_y:
                    light_found = True # if it is flip the light found toggle
                    # cv2.drawContours(frame, c, -1, (255, 0, 0), 3)
                    cv2.circle(frame, center, radius, (255, 0, 0), 4) #draw the cirlce
            else:
                light_found = False # toggle

        else: # no light found -- toggle
            light_found = False

        if light_found:
            newline = True
            if pause_timer.is_running(): #handle timer
                pause_timer.stop()

            if not light_timer.is_running():
                light_timer.start()
        else:
            # morse code decoding beyond this point!
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

        #draw the edges and original image (frame)
        cv2.imshow("edges", edges)
        cv2.imshow('frame', frame)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    print(light_array)
    cv2.destroyAllWindows()
    cap.release()

