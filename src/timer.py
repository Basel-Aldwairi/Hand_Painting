import time

class Timer:
    def __init__(self):

        self.color_switch = 0.75
        self.material_switch = 0.75
        self.stroke_timer = 0.5

        self.last_color_switch = time.time()
        self.last_material_switch = time.time()
        self.last_stroke = time.time()

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

    def connect_strokes(self):
        current_time = time.time()
        can_connect = False
        if current_time - self.last_stroke < self.stroke_timer:
            can_connect = True

        self.last_stroke = current_time
        return can_connect