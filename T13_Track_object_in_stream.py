""" ==== CREDITS ====

Cristian Moldovan
Departamentul de Mecatronica @ Facultatea de Mecanica UPT

"""

import cv2
import numpy as np

def nothing(x):
    pass

# --- setting the camera ---
cap = cv2.VideoCapture(0)

# --- getting the size of the camera ---
ret, first_frame = cap.read()
height, width = first_frame.shape[:2]
print(f"camera size (height x width): {height} x {width}")

# --- creating the output frame ---
WINDOW_RATIO = 0.6
output_window = np.zeros(((int)(height * WINDOW_RATIO), (int)(width * WINDOW_RATIO), 3), np.uint8)

frame_width = (int)(width * WINDOW_RATIO / 2)
frame_height = (int)(frame_width * height / width)

# --- creating the trackbars ---
cv2.namedWindow("Tracking")
cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LS", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
cv2.createTrackbar("UH", "Tracking", 255, 255, nothing)
cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

while True:
    # --- capturing the frame ---
    _, frame = cap.read()

    # --- changing from BGR to HSV format ---
    # OBS: OPENCV'S DEFAULT COLOR FORMAT IS BGR, NOT RGB
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # --- reading from the trackbars ---
    l_h = cv2.getTrackbarPos("LH", "Tracking")
    l_s = cv2.getTrackbarPos("LS", "Tracking")
    l_v = cv2.getTrackbarPos("LV", "Tracking")
    u_h = cv2.getTrackbarPos("UH", "Tracking")
    u_s = cv2.getTrackbarPos("US", "Tracking")
    u_v = cv2.getTrackbarPos("UV", "Tracking")

    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])

    # --- applying the masks ---
    mask = cv2.inRange(hsv, l_b, u_b)
    mask_canvas = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
    mask_canvas[:, :, 1] = mask
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # --- frames resizing ---
    output_frame = cv2.resize(frame, (frame_width, frame_height), interpolation=cv2.INTER_LINEAR)
    output_mask = cv2.resize(mask_canvas, (frame_width, frame_height), interpolation=cv2.INTER_LINEAR)
    output_res = cv2.resize(res, (frame_width, frame_height), interpolation=cv2.INTER_LINEAR)

    # --- adding text to each frame ---
    cv2.putText(output_frame, "Camera", (10, frame_height-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
    cv2.putText(output_mask, "Mask", (10, frame_height-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
    cv2.putText(output_res, "Result", (10, frame_height-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)

    output_window[0:frame_height, 0:frame_width] = output_mask
    output_window[0:frame_height, frame_width:(int)(width*WINDOW_RATIO)] = output_res
    output_window[frame_height:(int)(height*WINDOW_RATIO), ((int)(width * WINDOW_RATIO / 2) - (int)(frame_width / 2)):((int)(width * WINDOW_RATIO / 2) + (int)(frame_width / 2))] = output_frame


    # --- showing the output ---
    cv2.imshow("results", output_window)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
