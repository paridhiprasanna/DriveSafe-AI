import numpy as np

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]


class EyeDetector:

    def __init__(self):
        self.closed_frames = 0

    @staticmethod
    def euclidean(p1, p2):
        return np.linalg.norm(np.array(p1) - np.array(p2))

    def calculate_ear(self, eye_points):
        A = self.euclidean(eye_points[1], eye_points[5])
        B = self.euclidean(eye_points[2], eye_points[4])
        C = self.euclidean(eye_points[0], eye_points[3])

        return (A + B) / (2.0 * C)

    def get_ear(self, landmarks):
        left_eye = [landmarks[i] for i in LEFT_EYE]
        right_eye = [landmarks[i] for i in RIGHT_EYE]

        left_ear = self.calculate_ear(left_eye)
        right_ear = self.calculate_ear(right_eye)

        return (left_ear + right_ear) / 2

    def is_drowsy(self, ear, threshold=0.22):
        if ear < threshold:
            self.closed_frames += 1
        else:
            self.closed_frames = 0

        return self.closed_frames > 25