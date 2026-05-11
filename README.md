# Hand Tracking Drawing App

A real-time, interactive computer vision drawing application built with Python. This app tracks your hand landmarks to let you draw, erase, and change colors on the screen using simple hand gestures. Perfect for a futuristic game of Pictionary!

**Created by: Basel Al-Dwairi**

---

## Features & Controls

The app relies on different hand gestures to perform actions. Hold your hand up to the camera and use the following:

* **Index Finger Only:** Draw on the canvas.
* **Open Hand:** Erase (your palm acts as the eraser).
* **Ring + Pinky Fingers:** Open or close the color/size menu.
* **Index + Middle Fingers:** Show cursor and interact with the menu (select colors or change brush size).
* **Pinky Finger Only:** Switch brush material (Solid vs. Glassy).

---

## Prerequisites

Make sure you have Python installed. You will need to install the following libraries to run the app:

```bash
pip install opencv-python mediapipe numpy

```

---

## How to Run

1. Clone or download this repository.
2. Open your terminal or command prompt in the project folder.
3. Run the main file:

```bash
python main.py

```

4. **To exit the app:** Press `q` on your keyboard.

---

## Project Structure

* `main.py`: The main loop handling the camera feed and tying everything together.
* `hand_tracking.py`: Handles MediaPipe initialization and landmark detection.
* `gestures.py`: Evaluates finger positions to determine the active gesture.
* `painter.py`: Manages the canvas, drawing logic, masks, and the interactive menu.
* `timer.py`: Handles cooldowns (debouncing) so menus and colors don't flicker too quickly.
* `config.py`: Stores constants, settings, and Enums for colors, materials, and gestures.