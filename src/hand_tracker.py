import mediapipe as mp
import config

class HandTracker:

    def __init__(self, camera_resolution= config.CAMERA_RESOLUTION, monitor_resolution= config.MONITOR_RESOLUTION):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)
        self.mp_drawing = mp.solutions.drawing_utils

        self.camera_resolution = camera_resolution
        self.monitor_resolution = monitor_resolution


    def process_image(self, image):

        results = self.hands.process(image)

        landmarks = None

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            landmarks = hand_landmarks.landmark

        return landmarks

    def draw_landmarks(self, frame, landmarks):
        self.mp_drawing.draw_landmarks(frame, landmarks, self.mp_hands.HAND_CONNECTIONS)

        return frame