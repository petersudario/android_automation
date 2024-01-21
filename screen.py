import os
import time
import numpy as np
import pyautogui
import pygetwindow as gw
import cv2


class Screen:

    def __init__(self, device, device_number):
        self.device = device
        self.device_number = device_number
        self.model = device.get_model(device_number)

    def detect_images(self):
        window_title = f"{self.device_number}:{self.model}"

        os.system(".\\modules\\scrcpy\\scrcpy-noconsole.vbs --window-title=" + window_title)
        time.sleep(10)

        target_window = gw.getWindowsWithTitle(window_title)

        if not target_window:
            print(f"Window with title '{window_title}' not found.")
            return

        target_window[0].activate()
        try:
            while True:
                x, y, width, height = target_window[0].left, target_window[0].top, target_window[0].width, \
                    target_window[0].height

                background = pyautogui.screenshot(region=(x, y, width, height))
                background = np.array(background)
                background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

                frame = pyautogui.screenshot(region=(x, y, width, height))
                frame = np.array(frame)

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                diff = cv2.absdiff(background, gray)

                thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
                thresh = cv2.dilate(thresh, None, iterations=3)
                contours, res = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                for contour in contours:
                    if cv2.contourArea(contour) < 700:
                        continue
                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, "Status: {}".format("Motion Detected"), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 255), 3)
                cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

                cv2.imshow("Motion detection", frame)

                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
        except Exception as e:
            print(e)
        finally:
            cv2.destroyAllWindows()
