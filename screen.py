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

        while True:
            try:
                # Get the position and size of the target window
                x, y, width, height = target_window[0].left, target_window[0].top, target_window[0].width, \
                    target_window[0].height

                # Capture the screen region corresponding to the target window
                screenshot = pyautogui.screenshot(region=(x, y, width, height))
                screenshot = np.array(screenshot)

                # Convert the screenshot to BGR format
                frame = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

                # Motion detection logic
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (5, 5), 0)
                _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
                dilated = cv2.dilate(thresh, None, iterations=3)
                contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                for contour in contours:
                    (x, y, w, h) = cv2.boundingRect(contour)

                    if cv2.contourArea(contour) < 900:
                        continue
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, "Status: {}".format('In motion'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 255), 3)

                cv2.imshow("Motion Detection", frame)

                # Break the loop if 'Esc' key is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            except Exception as e:
                print(f"Error: {e}")
                break

        # Release resources
        cv2.destroyAllWindows()
