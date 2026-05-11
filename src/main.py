# Imports

import cv2
from config import CAMERA_RESOLUTION, MONITOR_RESOLUTION, LOW_POWER_CAMERA_RESOLUTION, USE_LOW_POWER_CAMERA
from hand_tracker import HandTracker
from gestures import get_marks, evaluate_gesture
from config import Gesture
from painter import Painter


# Open camera
cap = cv2.VideoCapture(0)

# Ser camera resolutions
if USE_LOW_POWER_CAMERA:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, LOW_POWER_CAMERA_RESOLUTION[1])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, LOW_POWER_CAMERA_RESOLUTION[0])
else:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_RESOLUTION[1])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_RESOLUTION[0])


# Initialize the hand tracking and painter objects
hand_tracker = HandTracker()
painter = Painter(brush_size=8)


# Main Loop
while True:

    # Read from camera
    success, frame = cap.read()
    if not success:
        break

    # preprocess the capruted frame so it can be drawn on
    # Frame gets fliped, change channels from BGR to RGB, as opencv uses BGR by default, and resize the frame to be the same resolution as the monitour
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, MONITOR_RESOLUTION)

    # Get hand landmarks from frame
    landmarks = hand_tracker.process_image(frame)

    # draw the handmarks
    hand_tracker.draw_hand_landmarks(frame)

    # if landmarks are detected
    if landmarks:

        # Evaluate the landmarks and the gesture
        marks = get_marks(landmarks)
        gesture = evaluate_gesture(marks)

        # Cursor location is the pointer fingertip
        pointer_tip = landmarks[8]

        # If the Gesture switched away from just the index finger (pointer finger), resert the cursor
        if gesture != Gesture.Index_Finger:
            painter.reset_previous_cursor()

        # Match the gesture to the appropraite action
        match gesture:
            # If only pointer finger is up, draw, unless the menu is shown
            case Gesture.Index_Finger:
                if not painter.show_menu:
                    painter.draw(pointer_tip)
                else:
                    pass
                    # painter.select_from_menu(landmarks[8])

            # If open hand, erase from the canvas
            case Gesture.Open_Hand:
                frame = painter.erase(frame, landmarks[0], landmarks[9])

            # If onlhy pinky finger is up, change materials, used to be change color
            case Gesture.Pinky_Finger:
                # painter.change_color()
                painter.change_material()

                pass

            # If ring finger is up, used to be change color
            case Gesture.Ring_Finger:
                pass
                # painter.open_menu()

            # If both Pointer and Middle fingers are up, draw the cursor, and select from the menu if menu is up
            case Gesture.Index_Middle_Fingers:
                painter.show_cursor(pointer_tip)
                if painter.show_menu:
                    painter.select_color_from_menu(pointer_tip)
                    painter.change_brush_size_from_menu(pointer_tip)

            # If ring and pinky fingers are up, open and close menu
            case Gesture.Ring_Pinky_Fingers:
                painter.toggle_menu()

    # If no hand is detected, reset the previous cursor
    else:
        painter.reset_previous_cursor()

    # Draw and update the frame
    frame = painter.update_frame(frame)

    # Write the name of the selected material, in the appropriate color
    cv2.putText(frame, painter.selected_material.name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, painter.selected_color.value, 2)

    # Return the frame back to BGR
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Show the newly updated and drawn frame
    cv2.imshow('frame', frame)

    # If 'q' is pressed, quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break