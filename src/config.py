from enum import Enum, auto


class Color(Enum):
    White = (255, 255, 255)
    Black = (0,0,0)
    Red = (255, 0, 0)
    Green = (0, 255, 0)
    Blue = (0, 0, 255)

class Material(Enum):
    Solid = 0
    Glassy = 1

class Gesture(Enum):

    Thumb = auto()
    Index_Finger = auto()
    Middle_Finger = auto()
    Ring_Finger = auto()
    Pinky_Finger = auto()

    Open_Hand = auto()
    Closed_Hand = auto()

    Index_Middle_Fingers = auto()

    Uknown = auto()

CAMERA_RESOLUTION = (360, 640)

LOW_POWER_CAMERA_RESOLUTION = (180, 320)

USE_LOW_POWER_CAMERA = False

MONITOR_RESOLUTION = (1920, 1080)



