import time

FINGER_TIPS = [4, 8, 12, 16, 20]


class GestureRecognizer:
    def __init__(self, hold_time=1.5):
        self.hold_time = hold_time
        self.start_time = None
        self.active = False

    def fingers_extended(self, lm):
        fingers = []

        # Thumb (x-axis comparison)
        fingers.append(1 if lm[4][1] > lm[3][1] else 0)

        # Other fingers (y-axis comparison)
        for tip in [8, 12, 16, 20]:
            fingers.append(1 if lm[tip][2] < lm[tip - 2][2] else 0)

        return fingers

    def detect_shutdown_gesture(self, lm):
        fingers = self.fingers_extended(lm)

        is_fist = fingers.count(1) == 0

        if is_fist:
            if not self.active:
                self.start_time = time.time()
                self.active = True

            elapsed = time.time() - self.start_time
            if elapsed >= self.hold_time:
                return True
        else:
            self.active = False
            self.start_time = None

        return False
