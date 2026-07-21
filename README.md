# AIr Painting

### *Turn your webcam into a canvas - paint on thin air with just your hand.*

AIr Painting is a real-time, gesture-controlled painting application built with **Python**, **OpenCV**, and **MediaPipe**. No mouse, no stylus, no touchscreen - just your hand, a webcam, and a virtual canvas that responds to your fingers. Draw, erase, switch materials, and pick colors, all through natural hand gestures tracked live from your camera feed.

---

## Project Overview

AIr Painting uses **MediaPipe Hands** to detect 21 hand landmarks per frame, then maps finger positions to a set of recognizable gestures (open hand, single fingers raised, finger combinations, etc.). Each gesture is bound to a painting action : drawing, erasing, changing brush material, or opening an on-screen color/brush menu.

Under the hood, the canvas is composited using bitwise masking tricks so that strokes persist across frames without needing to redraw the entire canvas from scratch, while still allowing smooth real-time performance.

---

## Key Features

-  **Real-time hand tracking** powered by MediaPipe Hands
-  **Freehand drawing** using just your index finger
-  **Palm-based eraser** that scales automatically with your hand size
-  **Two paint materials** - Solid and translucent "Glassy" (bitwise blend) strokes
- ️ **In-canvas interactive menu** for picking colors and adjusting brush size
- ️ **Built-in debounce/cooldown timers** to prevent accidental double-triggers
-  **Modular, extensible codebase** - add new colors, gestures, or materials with minimal changes

---

##  Supported Gestures & Actions

| Gesture | Hand Pose | Action |
|---|---|---|
| **Index Finger** |  Only index finger raised | Draw on the canvas |
| **Index + Middle Fingers** |  Index & middle raised | Show crosshair cursor; select color/brush size when menu is open |
| **Pinky Finger** | Only pinky raised | Toggle paint material (Solid ⇄ Glassy) |
| **Ring + Pinky Fingers** |  ring & pinky raised | Toggle the color & brush size menu open/closed |
| **Open Hand** |  All fingers raised | Erase - dynamically clears the canvas under your palm |
| **Closed Hand** | Fist | Idle (no action bound by default) |

> **Tip:** Gesture recognition is based on comparing fingertip and PIP-joint landmark positions (tip above pip = finger "up"). The thumb is intentionally excluded from tracking due to reliability issues, and is always treated as "down."

---

## Project Architecture

```text
.
├── README.md
├── requirements.txt
└── src
    ├── config.py          # Enums for colors, materials, gestures; display resolutions
    ├── gestures.py         # Hand landmark mark evaluation & gesture recognition logic
    ├── hand_tracker.py    # MediaPipe Hands wrapper class
    ├── main.py            # Primary application loop & frame rendering
    ├── painter.py          # Painting canvas, masking, brush sizes, glassy/solid materials, & UI menu logic
    ├── test.py            # Helper/test script
    └── timer.py            # Debounce/cooldown timers for gesture inputs
```

### Module Breakdown

| File | Responsibility |
|---|---|
| `config.py` | Central place for `Color`, `Material`, and `Gesture` enums, plus camera/monitor resolution constants |
| `gestures.py` | Converts raw hand landmarks into finger-up/down "marks," then maps those marks to a `Gesture` |
| `hand_tracker.py` | Thin wrapper around MediaPipe's `Hands` solution - processes frames and returns landmarks |
| `painter.py` | Owns the canvas, drawing mask, cursor, and menu rendering/hit-detection logic |
| `timer.py` | Provides cooldown checks (e.g. `can_material_switch`, `can_open_menu`) to debounce gesture triggers |
| `main.py` | Ties everything together: captures webcam frames, runs detection, dispatches gestures to `Painter` methods |

---

## Prerequisites & Installation

### Requirements
- Python **3.12+**
- A working webcam
- `pip` and (recommended) a virtual environment tool

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Basel-Aldwairi/Hand_Painting.git
   cd air-painting
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv

   # macOS / Linux
   source venv/bin/activate

   # Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   `requirements.txt` should include (at minimum):
   ```text
   opencv-python
   mediapipe
   numpy
   ```

---

## How to Run

Once dependencies are installed and your webcam is connected, launch the app:

```bash
python src/main.py
```

A window will open showing your live camera feed with the virtual canvas overlaid on top.

- Move your **index finger** to start drawing.
- Press **`q`** at any time to quit the application.

---

## Controls & Interaction Summary

| Action | How To |
|---|---|
| Draw | Raise only your index finger and move it around |
| Stop drawing / reset stroke | Change gesture away from index-only |
| Erase | Show an open palm near the canvas area you want to clear |
| Switch material (Solid ⇄ Glassy) | Raise only your pinky finger |
| Open/close color & brush menu | Raise your ring + pinky fingers together |
| Navigate menu / pick color / resize brush | Raise index + middle fingers and hover over menu items |
| Quit the app | Press **`q`** on your keyboard |

---

## How It Works (Under the Hood)

1. **Capture** - OpenCV grabs frames from the webcam, flips them for a mirror-like experience, and resizes to match the target monitor resolution.
2. **Track** - MediaPipe processes each frame and returns 21 hand landmarks (if a hand is detected).
3. **Interpret** - `gestures.py` evaluates fingertip vs. PIP-joint positions to build a boolean "marks" array, then matches it against known gesture patterns.
4. **Act** - `main.py` uses a `match` statement to route the detected gesture to the corresponding `Painter` method (draw, erase, change material, toggle menu, etc.).
5. **Render** - `painter.py` composites the canvas, drawing mask, cursor, and menu overlays using bitwise operations (`AND`, `OR`, `XOR`) for an efficient, layered rendering pipeline.

---

## Extending the Project

- **Add a new color:** Add an entry to the `Color` enum in `config.py` - it automatically appears in the on-screen color menu.
- **Add a new material:** Add an entry to the `Material` enum in `config.py`, then implement its rendering behavior in `Painter.draw()`.
- **Add a new gesture:** Define it in the `Gesture` enum, add a detection pattern in `gestures.py`, and bind it to an action in `main.py`.

---

## License

This project is open for personal and educational use. Feel free to fork, modify, and build on top of it.

---

<p align="center">Made with Python, OpenCV, and a bit of computer vision magic.</p>