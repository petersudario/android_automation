import cv2
import numpy as np
from mss import mss

# Initialize variables for motion detection
sct = mss()
monitor = sct.monitors[3]  # Assuming the primary monitor, adjust if needed

# Define the bounding box for the fourth quadrant
bounding_box = {
    'top': monitor['top'] + monitor['height'] // 2,
    'left': monitor['left'] + monitor['width'] // 2,
    'width': monitor['width'] // 2,
    'height': monitor['height'] // 2
}

frame1 = np.array(sct.grab(bounding_box))
frame2 = np.array(sct.grab(bounding_box))

while True:
    # Capture the fourth quadrant of the screen using mss
    sct_img = sct.grab(bounding_box)
    screen_frame = np.array(sct_img)

    # Apply motion detection on consecutive frames
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 900:
            continue
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)

    # Display the motion detection result
    image = cv2.resize(frame1, (1280, 720))
    cv2.imshow("feed", frame1)
    frame1 = frame2
    frame2 = np.array(sct_img)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(40) == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()
