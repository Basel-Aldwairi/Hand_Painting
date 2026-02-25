import cv2
from config import CAMERA_RESOLUTION, MONITOR_RESOLUTION, LOW_POWER_CAMERA_RESOLUTION, USE_LOW_POWER_CAMERA
from hand_tracker import HandTracker
from gestures import get_marks, evaluate_gesture
from config import Gesture
from painter import Painter

cap = cv2.VideoCapture(0)

if USE_LOW_POWER_CAMERA:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, LOW_POWER_CAMERA_RESOLUTION[1])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, LOW_POWER_CAMERA_RESOLUTION[0])
else:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_RESOLUTION[1])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_RESOLUTION[0])



hand_tracker = HandTracker()
painter = Painter()


while True:

    success, frame = cap.read()
    if not success:
        break


    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, MONITOR_RESOLUTION)

    landmarks = hand_tracker.process_image(frame)

    if landmarks:

        marks = get_marks(landmarks)
        gesture = evaluate_gesture(marks)

        if gesture != Gesture.Index_Finger:
            painter.reset_previous_cursor()

        match gesture:
            case Gesture.Index_Finger:
                painter.draw(landmarks[8])

            case Gesture.Open_Hand:
                frame = painter.erase(frame, landmarks[0], landmarks[9])

            case Gesture.Middle_Finger:
                painter.change_color()

            case Gesture.Pinky_Finger:
                # painter.change_material()
                painter.open_menu()

            case Gesture.Index_Middle_Fingers:
                painter.show_cursor(landmarks[8])

    else:
        painter.reset_previous_cursor()


    frame = painter.update_frame(frame)
    cv2.putText(frame, painter.selected_material.name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, painter.selected_color.value, 2)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break