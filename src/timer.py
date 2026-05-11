import time


class Timer:

    # Class for handeling all the timings

    # Initialize the used varialbles
    def __init__(self):

        # Minimum time to pass before performing certain actions in seconds
        self.color_switch = 0.75
        self.material_switch = 0.75
        self.open_menu = 0.75
        self.stroke_timer = 0.5
        self.color_switch_menu = 0.5
        self.brush_size_change = 0.15

        # Time of the last action performed in seconds (world clock)
        self.last_color_switch = time.time()
        self.last_material_switch = time.time()
        self.last_open_menu = time.time()
        self.last_stroke = time.time()
        self.last_color_switch_menu = time.time()
        self.last_brush_size_change = time.time()

    # Methods for calculating if enough time passed and updating the last action time
    # returns true if method can perform action otherwise false

    def can_color_switch(self):
        current_time = time.time()
        if current_time - self.last_color_switch > self.color_switch:
            self.last_color_switch = current_time
            return True
        return False

    def can_material_switch(self):
        current_time = time.time()
        if current_time - self.last_material_switch > self.material_switch:
            self.last_material_switch = current_time
            return True
        return False

    def can_open_menu(self):
        current_time = time.time()
        if current_time - self.last_open_menu > self.open_menu:
            self.last_open_menu = current_time
            return True
        return False

    def connect_strokes(self):
        current_time = time.time()
        can_connect = False
        if current_time - self.last_stroke < self.stroke_timer:
            can_connect = True

        self.last_stroke = current_time
        return can_connect

    def can_color_switch_menu(self):
        current_time = time.time()
        if current_time - self.last_color_switch_menu > self.color_switch_menu:
            self.last_color_switch_menu = current_time
            return True
        return False

    def can_thickness_switch(self):
        current_time = time.time()
        if current_time - self.last_brush_size_change > self.brush_size_change:
            self.last_brush_size_change = current_time
            return True
        return False
