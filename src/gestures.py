from config import Gesture
import numpy as np

# Functions to evaluate and return the marks needed from hand landmarks

# Simple helper function for similarity check
def evaluate_marks(required_marks, marks):
    return all(required_marks == marks)

# Process hand landmarks and return the correct marks
def get_marks(landmarks):
    # Initialize marks that will be calculated, False means that the finger is down, True means that the finger is up
    # Sequentially : Thumb, Pointer finger, Middle finger, Ring finger, Pinky finger
    marks = np.array([False, False, False, False, False], dtype=np.uint8)

    # Calculate Thumb position, deprecated, a lot of consistancy errors

    # thumb_tip = landmarks[4]
    # thumb_pip = landmarks[2]
    #
    # wrist = landmarks[0]

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

    # Thumb is always down when calculting
    marks[0] = False

    # Tips and Pips of the fingers, except for the thumb
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]

    finger_data = zip(tips, pips)

    # Iterate over all fingers, if tip is higher than the pip, the finger is up
    for i, (tip, pip) in enumerate(finger_data):
        if landmarks[tip].y < landmarks[pip].y:
            marks[i + 1] = True

    # if landmarks[tips[0]].z < landmarks[pips[0]].z:
    #     marks[1] = True
    #
    # marks[2] = False
    # marks[3] = False

    # Return the calculated marks
    return marks

# Map the marks to the correct gesture
def evaluate_gesture(marks) -> Gesture:

    gesture = Gesture.Uknown

    # Thumb, Pointer finger, Middle finger, Ring finger, Pinky finger
    # If true, the finger is Up, False the finger is down
    # The gestures are Enums from config.py

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

    elif evaluate_marks([False, False, False, True, True], marks):
        gesture =  Gesture.Ring_Pinky_Fingers


    return gesture

