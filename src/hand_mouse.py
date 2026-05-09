import cv2
from config import CAMERA_RESOLUTION, MONITOR_RESOLUTION, LOW_POWER_CAMERA_RESOLUTION, USE_LOW_POWER_CAMERA
from hand_tracker import HandTracker
from gestures import get_marks, evaluate_gesture
from config import Gesture
from pynput.mouse import Button, Controller

mouse = Controller()

cap = cv2.VideoCapture(0)

if USE_LOW_POWER_CAMERA:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, LOW_POWER_CAMERA_RESOLUTION[1])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, LOW_POWER_CAMERA_RESOLUTION[0])
else:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_RESOLUTION[1])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_RESOLUTION[0])



hand_tracker = HandTracker()
held_left_button = False

while True:

    success, frame = cap.read()
    if not success:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, MONITOR_RESOLUTION)

    landmarks = hand_tracker.process_image(frame)

    if landmarks:

        marks = get_marks(landmarks)
        gesture = evaluate_gesture(marks)

        if gesture == Gesture.Index_Finger or gesture == Gesture.Index_Middle_Fingers:

            index_finger = landmarks[8]
            x = index_finger.x * MONITOR_RESOLUTION[0]
            y = index_finger.y * MONITOR_RESOLUTION[1]

            mouse.position = (x, y)

        if gesture == Gesture.Index_Middle_Fingers:
            mouse.press(Button.left)
            mouse.release(Button.left)

    # sframe = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # cv2.imshow('frame', sframe)