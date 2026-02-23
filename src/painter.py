import cv2
import numpy as np
from config import MONITOR_RESOLUTION, Color, Material
import timer

class Painter:
    def __init__(self, monitor_resolution= MONITOR_RESOLUTION, thickness=8):

        self.monitor_resolution = monitor_resolution

        self.canvas = np.zeros(shape=(self.monitor_resolution[1], self.monitor_resolution[0], 3), dtype="uint8")
        self.mask = np.zeros_like(self.canvas)
        self.mask.fill(255)

        self.thickness = thickness

        self.colors = [Color.White, Color.Black, Color.Red, Color.Green, Color.Blue]
        self.color_index = 0
        self.selected_color = self.colors[self.color_index]

        self.material_index = 0
        self.materials = [Material.Solid, Material.Glassy]
        self.selected_material = self.materials[self.material_index]

        self.previous_cursor = None

        self.timer = timer.Timer()

    def update_frame(self, frame):
        new_frame = (frame & self.mask) + self.canvas
        return new_frame


    def draw(self, frame, cursor):

        h, w , c = self.canvas.shape
        cx, cy = int(cursor.x * w), int(cursor.y * h)

        stroke = np.zeros_like(self.canvas)

        if not self.previous_cursor or not self.timer.connect_strokes():
            self.previous_cursor = (cx ,cy)

        if self.selected_material == Material.Solid:
            cv2.circle(self.canvas, (cx, cy), self.thickness, self.selected_color.value, cv2.FILLED)
            cv2.line(self.canvas, (cx, cy), self.previous_cursor, self.selected_color.value, int(self.thickness * 2))

        elif self.selected_material == Material.Glassy:
            cv2.circle(stroke, (cx, cy), self.thickness, self.selected_color.value, cv2.FILLED)
            cv2.line(stroke, (cx, cy), self.previous_cursor, self.selected_color.value, int(self.thickness * 2))

        cv2.circle(self.mask, (cx, cy), self.thickness, (0, 0, 0), cv2.FILLED)
        cv2.line(self.mask, (cx, cy), self.previous_cursor, (0, 0, 0), int(self.thickness * 2))

        self.previous_cursor = (cx, cy)

        if self.selected_material == Material.Glassy:
            cv2.bitwise_or(self.canvas, stroke, self.canvas)


    def show_cursor(self, frame, cursor):
        pass


    def erase(self, frame, wrist, middle_base):

        h, w , c = self.canvas.shape

        eraser_x = int((wrist.x * w + middle_base.x * w) / 2)
        eraser_y = int((wrist.y * h + middle_base.y * h) / 2)

        eraser_radius = int(
            (((wrist.x * w - middle_base.x * w) ** 2 + (wrist.y * h - middle_base.y * h) ** 2) ** 0.5) / 2)

        cv2.circle(frame, (eraser_x, eraser_y), eraser_radius, (0, 0, 0), 1)
        cv2.circle(self.canvas, (eraser_x, eraser_y), eraser_radius, (0, 0, 0), cv2.FILLED)
        cv2.circle(self.mask, (eraser_x, eraser_y), eraser_radius, (255, 255, 255), cv2.FILLED)

        return self.update_frame(frame)

    def change_color(self):

        if self.timer.can_color_switch():
            self.color_index = (self.color_index + 1) % len(self.colors)
            self.selected_color = self.colors[self.color_index]

    def change_material(self):
        if self.timer.can_material_switch():
            self.material_index = (self.material_index + 1) % len(self.materials)
            self.selected_material = self.materials[self.material_index]

    def reset_previous_cursor(self):
        self.previous_cursor = None