import cv2
import numpy as np
from config import MONITOR_RESOLUTION, Color, Material
import timer


class Painter:

    # Pinter function that handles the Canvas and all the painting mathematics

    # Initialize all the used parameters
    def __init__(self, monitor_resolution=MONITOR_RESOLUTION, brush_size=8):

        # Monitor resolution for consistancy
        self.monitor_resolution = monitor_resolution

        # Canvas and mask arrays
        self.canvas = np.zeros(shape=(self.monitor_resolution[1], self.monitor_resolution[0], 3), dtype="uint8")
        self.mask = np.zeros_like(self.canvas)
        self.mask.fill(255)

        # Brush and cursor size
        self.brush_size = brush_size
        self.cursor_thickness = 4
        self.max_brush_size = 30
        self.min_brush_size = 1

        # Color list and selected color
        self.colors = [color for color in Color]
        self.color_index = 0
        self.selected_color = self.colors[self.color_index]

        # Materials and selected material
        self.material_index = 0
        self.materials = [material for material in Material]
        self.selected_material = self.materials[self.material_index]

        # Pervious cursor location for connecting dots
        self.previous_cursor = None

        # Timer object for timing and logic flow
        self.timer = timer.Timer()

        # Cursor array to draw cursor
        self.cursor_array = np.zeros_like(self.canvas)

        # Color Menu arrays to draw the Menu
        self.color_menu = np.zeros_like(self.canvas)
        self.color_menu_mask = np.zeros_like(self.canvas)
        self.color_menu_mask.fill(255)
        self.show_menu = False

        # Cursor menu arrays to draw the Menu
        self.cursor_menu = np.zeros_like(self.canvas)
        self.cursor_menu_mask = np.zeros_like(self.canvas)
        self.cursor_menu_mask.fill(255)

        # Menu drawing and hit detection variables
        self.rectangle_size = 100
        self.offest = 125
        self.x_begin = 50
        self.y_begin = 50
        self.colors_in_row = 5
        self.fill_menu()


    # Update Frame, Calculates and return the new frame
    def update_frame(self, frame):
        # The new frame is calculated as follows:
        # The Frame from the camera is bit-wise anded with the canvas mask, then added to the canvas so the colors appear
        new_frame = ((frame & self.mask) + self.canvas)

        # If the menu is open, do the same but with the menu mask and the menu arrays
        if self.show_menu:
            new_frame = (new_frame & self.color_menu_mask) + self.color_menu

            self.cursor_size_menu()
            new_frame = (new_frame & self.cursor_menu_mask) + self.cursor_menu

        # If the cursor is show, bit-wise xor the cursor array, so the cursor is always visable
        new_frame = new_frame ^ self.cursor_array

        # Reset the cursor array
        self.cursor_array.fill(0)


        return new_frame

    # Main Drawing function
    def draw(self, cursor):


        # Get the cursor location, which is the tip of the pointer finger
        h, w, c = self.canvas.shape
        cx, cy = int(cursor.x * w), int(cursor.y * h)

        # Stroke array to calculate the stroke made
        stroke = np.zeros_like(self.canvas)

        # If this is the start of a new stroke, the previous cursor is set to this cursor, to make the functions easier
        if not self.previous_cursor or not self.timer.connect_strokes():
            self.previous_cursor = (cx, cy)

        # If the material is Solid, draw a circle on the cursor location, and a line connecting the last stroke as well
        if self.selected_material == Material.Solid:
            cv2.circle(self.canvas, (cx, cy), self.brush_size, self.selected_color.value, cv2.FILLED)
            cv2.line(self.canvas, (cx, cy), self.previous_cursor, self.selected_color.value, int(self.brush_size * 2))

        # If the material is Glassy, draw the cursor location and the stroke on the stroek array, to be bit-wise ored with the canvas to give the glassy effect
        elif self.selected_material == Material.Glassy:
            cv2.circle(stroke, (cx, cy), self.brush_size, self.selected_color.value, cv2.FILLED)
            cv2.line(stroke, (cx, cy), self.previous_cursor, self.selected_color.value, int(self.brush_size * 2))

        # Draw the same Circle and line on the mask array, so we can mask the frame and add the canvas to it
        cv2.circle(self.mask, (cx, cy), self.brush_size, (0, 0, 0), cv2.FILLED)
        cv2.line(self.mask, (cx, cy), self.previous_cursor, (0, 0, 0), int(self.brush_size * 2))

        # Set the previous cursor to the currect cursor
        self.previous_cursor = (cx, cy)

        # Bit-wise or for the Glassy effect
        if self.selected_material == Material.Glassy:
            cv2.bitwise_or(self.canvas, stroke, self.canvas)



    # Show cursor function incase the cursor should be shown
    def show_cursor(self, cursor):

        cursor_width = self.brush_size

        # Get cursor location
        h, w, c = self.canvas.shape
        cx, cy = int(cursor.x * w), int(cursor.y * h)

        # Draw a '+' symbol on the cursor (fingertip) on the canvas and the mask arrays
        # Size of the cursor would be the same as the brush size, the thickness can be adjusted in code, chosen through testing
        cv2.line(self.cursor_array, (cx - cursor_width, cy), (cx + cursor_width, cy), Color.White.value,
                 self.cursor_thickness)
        cv2.line(self.cursor_array, (cx, cy - cursor_width), (cx, cy + cursor_width), Color.White.value,
                 self.cursor_thickness)


    # Erase function, erases anything on the palm of the hand, adjusts automatically
    def erase(self, frame, wrist, middle_base):

        # Get the middle of the erasur circle, which will be between the wrist and the base of the middle finger (the palm of the hand)
        h, w, c = self.canvas.shape

        eraser_x = int((wrist.x * w + middle_base.x * w) / 2)
        eraser_y = int((wrist.y * h + middle_base.y * h) / 2)

        # Calculate the radious (size of the palm in the frame)
        eraser_radius = int(
            (((wrist.x * w - middle_base.x * w) ** 2 + (wrist.y * h - middle_base.y * h) ** 2) ** 0.5) / 2)

        # Erase and reset both the canvas and the mask
        cv2.circle(frame, (eraser_x, eraser_y), eraser_radius, (0, 0, 0), 1)
        cv2.circle(self.canvas, (eraser_x, eraser_y), eraser_radius, (0, 0, 0), cv2.FILLED)
        cv2.circle(self.mask, (eraser_x, eraser_y), eraser_radius, (255, 255, 255), cv2.FILLED)

        return self.update_frame(frame)


    # Change color, Deprecated, added color switch to menu
    def change_color(self):

        # If enough time passed since last color switch, you can color switch
        if self.timer.can_color_switch():
            self.color_index = (self.color_index + 1) % len(self.colors)
            self.selected_color = self.colors[self.color_index]

    # Change material type
    def change_material(self):

        # If enough time passed since last material siwtch, you can material switch
        if self.timer.can_material_switch():
            self.material_index = (self.material_index + 1) % len(self.materials)
            self.selected_material = self.materials[self.material_index]

    # Reset previous cursor function
    def reset_previous_cursor(self):
        self.previous_cursor = None

    # Toggle menu function
    def toggle_menu(self):

        # If enough time passed since last menu open and close, you can open or close the menu
        if self.timer.can_open_menu():
            self.show_menu = not self.show_menu


    # Get coordinates for the color boxes in the menus
    def get_coordinates(self, index):

        x_index = index % self.colors_in_row
        x_start = self.x_begin + self.offest * x_index
        x_end = x_start + self.rectangle_size

        y_index = int(np.floor(index / self.colors_in_row))
        y_start = self.y_begin + self.offest * y_index
        y_end = y_start + self.rectangle_size

        return (x_start, y_start), (x_end, y_end)


    # Draw the color menu
    def fill_menu(self):

        # Iterate over all colors in the colors list
        for i, color in enumerate(self.colors):

            # Get the box coordinates
            start, end = self.get_coordinates(i)

            # Draw the box in the correct color
            cv2.rectangle(self.color_menu, start, end, color.value,
                          cv2.FILLED)
            cv2.rectangle(self.color_menu_mask, start, end, (0, 0, 0),
                          cv2.FILLED)


    # Draw cursor change size menu
    # Needs to be optimized down the line
    def cursor_size_menu(self):

        h, w, c = self.canvas.shape

        # Get coordinats of where the box should be
        y_start = self.y_begin + self.offest
        x_start = w - self.x_begin - self.offest - self.rectangle_size

        # Reset menu arrays, needs to be optimised
        self.cursor_menu.fill(0)
        self.cursor_menu_mask.fill(255)

        # Calculate the box corners
        x_rect_start = x_start - self.rectangle_size // 2
        x_rect_end = x_start + self.rectangle_size // 2
        y_rect_start = y_start - 3 * self.rectangle_size // 2 + (self.offest - self.rectangle_size)
        y_rect_end = y_rect_start + 3 * self.offest - (self.offest - self.rectangle_size)

        # Calculate the center of the box
        cy = (y_rect_start + y_rect_end) // 2
        cx = (x_rect_end + x_rect_start) // 2

        # Draw the Box menu
        cv2.rectangle(self.cursor_menu_mask, (x_rect_start - 2, y_rect_start - 2), (x_rect_end + 2, y_rect_end + 2),
                      Color.Black.value, cv2.FILLED)
        cv2.rectangle(self.cursor_menu, (x_rect_start, y_rect_start), (x_rect_end, y_rect_end), Color.White.value,
                      cv2.FILLED)

        # Draw the seperation lines in the box
        cv2.rectangle(self.cursor_menu, (cx - self.rectangle_size // 2, cy + self.rectangle_size // 2 - 1),
                      (cx + self.rectangle_size // 2, cy + self.rectangle_size // 2 + 1), Color.Black.value,
                      cv2.FILLED)
        cv2.rectangle(self.cursor_menu, (cx - self.rectangle_size // 2, cy - self.rectangle_size // 2 - 1),
                      (cx + self.rectangle_size // 2, cy - self.rectangle_size // 2 + 1), Color.Black.value,
                      cv2.FILLED)

        # Get center and the rough center of the upper and lower boxes
        center = (2 * self.offest + self.rectangle_size) // 3
        cy_top = cy - center
        cy_bot = cy + center


        # Symbol drawing variables, chosen through testing
        symbol_thickness = 4
        offset_measurement = 5

        # Draw the '-' symbol in the lower box
        cv2.rectangle(self.cursor_menu,
                      (cx - self.rectangle_size // 2 + self.offest // offset_measurement, cy_bot - symbol_thickness),
                      (cx + self.rectangle_size // 2 - self.offest // offset_measurement, cy_bot + symbol_thickness),
                      Color.Black.value,
                      cv2.FILLED)

        # Draw the '+' in the upper box
        cv2.rectangle(self.cursor_menu,
                      (cx - self.rectangle_size // 2 + self.offest // offset_measurement, cy_top - symbol_thickness),
                      (cx + self.rectangle_size // 2 - self.offest // offset_measurement, cy_top + symbol_thickness),
                      Color.Black.value,
                      cv2.FILLED)
        cv2.rectangle(self.cursor_menu,
                      (cx - symbol_thickness, cy_top - self.rectangle_size // 2 + self.offest // offset_measurement),
                      (cx + symbol_thickness, cy_top + self.rectangle_size // 2 - self.offest // offset_measurement),
                      Color.Black.value,
                      cv2.FILLED)


        # Draw the cursor with the appropriate size and color in the middle box
        cv2.circle(self.cursor_menu, (cx, cy), self.brush_size + 1, Color.Black.value, cv2.FILLED)
        cv2.circle(self.cursor_menu, (cx, cy), self.brush_size, self.selected_color.value, cv2.FILLED)


    # Select color from menu function
    def select_color_from_menu(self, cursor):

        # Get cursor location
        h, w, c = self.canvas.shape
        cx, cy = int(cursor.x * w), int(cursor.y * h)

        # Inumarate over all the color boxes
        for i, color in enumerate(self.colors):

            # Get the location and corners of the color boxes
            start, end = self.get_coordinates(i)
            x_start, y_start = start
            x_end, y_end = end

            # If cursor is inside the box location, update cursor and close the menu
            if x_start <= cx <= x_end and y_start <= cy <= y_end:
                if color != self.selected_color:
                    self.selected_color = color
                    self.show_menu = False


    # Change brush size from menu, needs to be optimzes
    def change_brush_size_from_menu(self, cursor):

        # Get cursor location
        h, w, c = self.canvas.shape
        cx, cy = int(cursor.x * w), int(cursor.y * h)

        # Calculate the box locations for the '+' and '-' symbols, needs to be optimized
        y_start = self.y_begin + self.offest
        x_start = w - self.x_begin - self.offest - self.rectangle_size

        x_rect_start = x_start - self.rectangle_size // 2
        x_rect_end = x_start + self.rectangle_size // 2
        y_rect_start = y_start - 3 * self.rectangle_size // 2 + (self.offest - self.rectangle_size)
        y_rect_end = y_rect_start + 3 * self.offest - (self.offest - self.rectangle_size)

        x_start_rectangle = x_rect_start
        x_end_rectangle  = x_rect_end
        y_start_plus_rectangle = y_rect_start
        y_end_plus_rectangle = y_start_plus_rectangle + self.rectangle_size

        y_end_minus_rectangle = y_rect_end
        y_start_minus_rectangle = y_rect_end - self.rectangle_size


        # If enough time passed since last brush size change, change the brush size
        if self.timer.can_thickness_switch():

            # If cursor is detected inside the '+' symbol box, increase the brush size
            if x_start_rectangle <= cx <= x_end_rectangle and y_start_plus_rectangle <= cy <= y_end_plus_rectangle:
                self.brush_size += 1
                if self.brush_size >= self.max_brush_size:
                    self.brush_size = self.max_brush_size

            # If cursor is detected inside the '-' symbol box, decrease the brush size
            if x_start_rectangle <= cx <= x_end_rectangle and y_start_minus_rectangle <= cy <= y_end_minus_rectangle:
                self.brush_size -= 1
                if self.brush_size <= self.min_brush_size:
                    self.brush_size = self.min_brush_size

