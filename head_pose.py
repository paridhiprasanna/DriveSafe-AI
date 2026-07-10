import cv2
import numpy as np


class HeadPoseEstimator:

    def __init__(self):
        self.offroad_frames = 0
        self.allowed_frames = 45   # about 1.5 seconds

    def estimate(self, frame, landmarks):

        image_points = np.array([
            landmarks[1],     # Nose
            landmarks[152],   # Chin
            landmarks[33],    # Left eye
            landmarks[263],   # Right eye
            landmarks[61],    # Left mouth
            landmarks[291]    # Right mouth
        ], dtype="double")

        h, w = frame.shape[:2]

        model_points = np.array([
            (0.0, 0.0, 0.0),
            (0.0, -330.0, -65.0),
            (-225.0, 170.0, -135.0),
            (225.0, 170.0, -135.0),
            (-150.0, -150.0, -125.0),
            (150.0, -150.0, -125.0)
        ])

        focal_length = w
        center = (w / 2, h / 2)

        camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype="double")

        dist_coeffs = np.zeros((4, 1))

        success, rotation_vector, translation_vector = cv2.solvePnP(
            model_points,
            image_points,
            camera_matrix,
            dist_coeffs
        )

        if not success:
            return "Unknown"

        rmat, _ = cv2.Rodrigues(rotation_vector)

        angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)

        pitch = angles[0]
        yaw = angles[1]
        if pitch > 90:
            pitch -= 180
        elif pitch < -90:
            pitch += 180

        print(f"Pitch={pitch:.2f}, Yaw={yaw:.2f}")

        # Wider thresholds
        distracted = (
            yaw > 30 or
            yaw < -30 or
            pitch > 25 or
            pitch < -20
        )

        if distracted:
            self.offroad_frames += 1
        else:
            self.offroad_frames = 0
            return "Forward"

        # Ignore short glances
        if self.offroad_frames < self.allowed_frames:
            return "Forward"

        if yaw > 30:
            return "Looking Right"

        elif yaw < -30:
            return "Looking Left"

        elif pitch > 20:
            return "Looking Down"

        elif pitch < -20:
            return "Looking Up"

        return "Forward"