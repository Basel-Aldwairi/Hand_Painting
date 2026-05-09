from enum import Enum, auto


class Color(Enum):
    White = (255, 255, 255)
    Black = (0,0,0)
    Red = (255, 0, 0)
    Green = (0, 255, 0)
    Blue = (0, 0, 255)
    Pink = (255, 92, 119)
    Teal =  (0,128,128)
    Gray_80 = (204,204,204)
    Gray_20 = (51,51,51)
    Dark_Maroon = (85,0,0)
    Aquamarine =  (102,204,204)
    Spring_Green  = (0,255,127)
    Peach =  (255,102,102)
    Dark_Teal =  (19,51,55)
    Dark_Green =  (6,85,53)
    Cyan =  (0,255,255)
    Orange =  (255,165,0)
    Gold =  (255,215,0)
    Turquoise =  (64,224,208)
    Misty_Rose =  (255,228,225)
    Midnight_Blue =  (0,51,102)
    Maroon = (85,0,0)
    Patriarch_Purple =  (128,0,128)


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
    Ring_Pinky_Fingers = auto()

    Uknown = auto()

CAMERA_RESOLUTION = (360, 640)

LOW_POWER_CAMERA_RESOLUTION = (180, 320)

USE_LOW_POWER_CAMERA = False

MONITOR_RESOLUTION = (1920, 1080)
# MONITOR_RESOLUTION = (1920//2, 1080//2)



