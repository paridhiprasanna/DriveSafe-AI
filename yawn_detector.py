import numpy as np

UPPER_LIP = 13
LOWER_LIP = 14

LEFT_MOUTH = 78
RIGHT_MOUTH = 308


class YawnDetector:

    def __init__(self):
        self.open_frames = 0
        self.required_frames = 30   # About 1 second at 30 FPS

    @staticmethod
    def distance(p1, p2):
        return np.linalg.norm(np.array(p1) - np.array(p2))

    def mouth_aspect_ratio(self, landmarks):

        vertical = self.distance(
            landmarks[UPPER_LIP],
            landmarks[LOWER_LIP]
        )

        horizontal = self.distance(
            landmarks[LEFT_MOUTH],
            landmarks[RIGHT_MOUTH]
        )

        mar = vertical / horizontal
        return mar

    def is_yawning(self, mar):

        # Increased threshold
        threshold = 0.08

        if mar > threshold:
            self.open_frames += 1
        else:
            self.open_frames = 0

        # Mouth must stay open for ~1 second
        if self.open_frames >= self.required_frames:
            return True

        return False