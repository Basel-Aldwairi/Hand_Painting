from config import Gesture
import numpy as np

def evaluate_marks(required_marks, marks):
    return all(required_marks == marks)

def get_marks(landmarks):
    marks = np.array([False, False, False, False, False], dtype=np.uint8)

    thumb_tip = landmarks[4]
    thumb_pip = landmarks[2]

    wrist = landmarks[0]

    # if wrist.x > thumb_pip.x:
    #     if thumb_tip.x < thumb_pip.x:
    #         marks[0] = True
    #     else:
    #         marks[0] = False
    # else:
    #     if thumb_tip.x > thumb_pip.x:
    #         marks[0] = True
    #     else:
    #         marks[0] = False

    marks[0] = False

    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]

    finger_data = zip(tips, pips)

    for i, (tip, pip) in enumerate(finger_data):
        if landmarks[tip].y < landmarks[pip].y:
            marks[i + 1] = True

    return marks

def evaluate_gesture(marks) -> Gesture:

    gesture = Gesture.Uknown

    if evaluate_marks([True, False, False, False, False], marks):
        gesture = Gesture.Thumb

    elif evaluate_marks([False, True, False, False, False], marks):
        gesture =  Gesture.Index_Finger

    elif evaluate_marks([False, False, True, False, False], marks):
        gesture =  Gesture.Middle_Finger

    elif evaluate_marks([False, False, False, True, False], marks):
        gesture = Gesture.Ring_Finger

    elif evaluate_marks([False, False, False, False, True], marks):
        gesture = Gesture.Pinky_Finger

    elif evaluate_marks([False, False, False, False, False], marks):
        gesture = Gesture.Closed_Hand

    elif evaluate_marks([False, True, True, True, True], marks):
        gesture = Gesture.Open_Hand

    elif evaluate_marks([False, True, True, False, False], marks):
        gesture =  Gesture.Index_Middle_Fingers


    return gesture

