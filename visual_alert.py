import cv2

class VisualAlert:

    def draw_alert(
        self,
        frame,
        risk_score,
        risk_level
    ):

        h, w = frame.shape[:2]

        overlay = frame.copy()

        cv2.rectangle(
            overlay,
            (0, 0),
            (w, 100),
            (0, 0, 255),
            -1
        )

        cv2.addWeighted(
            overlay,
            0.3,
            frame,
            0.7,
            0,
            frame
        )

        cv2.putText(
            frame,
            f"RISK: {risk_score}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"LEVEL: {risk_level}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

        return frame