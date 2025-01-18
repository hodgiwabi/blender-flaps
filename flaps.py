import bpy
from math import pi

# Parameters
FLAPS = 10
SHAFTS = ["Circle", "Circle.001", "Circle.002", "Circle.003"]
FRAMES_PER_DIGIT = 10
FRAMES_PER_PAUSE = 20
NUMBERS_TO_DISPLAY = [1234, 4235, 2012, 2345, 1999, 782]

class FlapDisplay:
    def __init__(self):
        self.current_digits = [0 for _ in SHAFTS]
        self.frame_count = 1

    def clear_animation_data(self):
        """Clear existing animation data from all shafts"""
        for shaft_name in SHAFTS:
            obj = bpy.data.objects.get(shaft_name)
            if obj:
                obj.animation_data_clear()

    def pin_to_current_frame(self, frame_count):
        """Insert keyframe for current rotation on all shafts"""
        for shaft_name in SHAFTS:
            obj = bpy.data.objects.get(shaft_name)
            if obj:
                obj.keyframe_insert(data_path="rotation_euler", frame=frame_count, index=1)

    def display_number(self, number):
        """Set rotation for each shaft to display given number"""
        for i, shaft_name in enumerate(SHAFTS):
            self.current_digits[i] = number % FLAPS
            number = number // FLAPS
            obj = bpy.data.objects.get(shaft_name)
            if obj:
                obj.rotation_euler.y = self.to_radians(-360/FLAPS * self.current_digits[i])

    @staticmethod
    def to_radians(angle):
        """Convert degrees to radians"""
        return angle * pi / 180

    def make_interpolation_linear(self):
        """Set all keyframes to linear interpolation"""
        for shaft_name in SHAFTS:
            obj = bpy.data.objects.get(shaft_name)
            if obj and obj.animation_data and obj.animation_data.action:
                for fcurve in obj.animation_data.action.fcurves:
                    for kf in fcurve.keyframe_points:
                        kf.interpolation = 'LINEAR'

    def animate_sequence(self):
        """Animate the complete sequence of numbers"""
        self.clear_animation_data()

        # Display initial number
        self.display_number(NUMBERS_TO_DISPLAY[0])
        self.pin_to_current_frame(self.frame_count)

        # Animate transitions between numbers
        for next_number in NUMBERS_TO_DISPLAY[1:]:
            while True:
                new_number = next_number
                done = True

                for j, shaft_name in enumerate(SHAFTS):
                    new_digit = new_number % FLAPS
                    new_number = new_number // FLAPS

                    if new_digit != self.current_digits[j]:
                        done = False
                        self.current_digits[j] = (self.current_digits[j] + 1) % FLAPS
                        obj = bpy.data.objects.get(shaft_name)
                        if obj:
                            obj.rotation_euler.y -= self.to_radians(360/FLAPS)

                self.frame_count += FRAMES_PER_DIGIT
                self.pin_to_current_frame(self.frame_count)

                if done:
                    break

            self.frame_count += FRAMES_PER_PAUSE
            self.pin_to_current_frame(self.frame_count)

        # Set linear interpolation and update scene frame range
        self.make_interpolation_linear()
        if bpy.context.scene:
            bpy.context.scene.frame_end = self.frame_count

def main():
    flap_display = FlapDisplay()
    flap_display.animate_sequence()

if __name__ == "__main__":
    main()
