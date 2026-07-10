# main.py
import cv2

from face_mesh import FaceMeshDetector
from eye_detector import EyeDetector
from yawn_detector import YawnDetector
from head_pose import HeadPoseEstimator
from risk_engine import RiskEngine
from audio_alert import AudioAlert
from visual_alert import VisualAlert
from break_recommendation import BreakRecommendation

from database import init_db, log_event

# ----------------------------
# INITIALIZATION
# ----------------------------

init_db()

face_detector = FaceMeshDetector()
eye_detector = EyeDetector()
yawn_detector = YawnDetector()
head_pose_estimator = HeadPoseEstimator()

risk_engine = RiskEngine()
break_engine = BreakRecommendation()

audio_alert = AudioAlert()
visual_alert = VisualAlert()

cap = cv2.VideoCapture(0)

print("DriveSafe AI Started...")


# ----------------------------
# MAIN LOOP
# ----------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    landmarks = face_detector.get_landmarks(frame)

    if landmarks:

        # ----------------------------
        # EYE DETECTION
        # ----------------------------

        ear = eye_detector.get_ear(landmarks)
        drowsy = eye_detector.is_drowsy(ear)

        # ----------------------------
        # YAWN DETECTION
        # ----------------------------

        mar = yawn_detector.mouth_aspect_ratio(landmarks)
        yawning = yawn_detector.is_yawning(mar)

        # ----------------------------
        # HEAD POSE
        # ----------------------------

        direction = head_pose_estimator.estimate(
            frame,
            landmarks
        )
        print(
            f"Direction: {direction} | "
            f"Risk: {risk_score if 'risk_score' in locals() else 0}"
        )

        # ----------------------------
        # RISK CALCULATION
        # ----------------------------
       
        risk_score = risk_engine.calculate_risk(
            drowsy=drowsy,
            yawning=yawning,
            head_pose=direction
        )

        risk_level = risk_engine.get_risk_level(
            risk_score
        )
        safety_score = 100 - risk_score
        print("----------------------")
        print("Drowsy:", drowsy)
        print("Yawning:", yawning)
        print("Head Pose:", direction)
        print("Risk:", risk_score)
        # ----------------------------
        # BREAK RECOMMENDATION
        # ----------------------------

        break_engine.update(risk_score)

        take_break, break_message = (
            break_engine.recommend()
        )
        if risk_score < 30:
            recommendation = "Drive Safe"
        elif risk_score < 60:
            recommendation = "Stay Alert"
        else:
            recommendation = "Take a Break"
        # ----------------------------
        # AUDIO ALERT
        # ----------------------------

        if risk_score >= 75:
            audio_alert.play()
        else:
            audio_alert.stop()

    

        # ----------------------------
        # DATABASE LOGGING
        # ----------------------------

        log_event(
            ear,
            mar,
            direction,
            risk_score,
            risk_level,
            drowsy,
            yawning
        )

        # ----------------------------
        # VISUAL ALERT PANEL
        # ----------------------------

        frame = visual_alert.draw_alert(
            frame,
            risk_score,
            risk_level
        )

        # ----------------------------
        # DISPLAY METRICS
        # ----------------------------
        cv2.putText(
            frame,
            f"Safety Score: {safety_score}",
            (20,120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,255),
            2
        )

        cv2.putText(
            frame,
            f"Risk Level: {risk_level}",
            (20,90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,255),
            2
        )
        cv2.putText(
            frame,
            f"EAR: {ear:.2f}",
            (20, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"MAR: {mar:.2f}",
            (20, 190),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Head Pose: {direction}",
            (20, 230),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )

        # ----------------------------
        # DRIVER STATE
        # ----------------------------

        if drowsy:

            cv2.putText(
                frame,
                "DROWSY DETECTED",
                (20, 280),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 0, 255),
                3
            )

        if yawning:

            cv2.putText(
                frame,
                "YAWNING",
                (20, 330),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 0, 255),
                3
            )

        if direction in ["Looking Left", "Looking Right"]:

            cv2.putText(
                frame,
                "DISTRACTION DETECTED",
                (20, 380),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 0, 255),
                3
            )

        # ----------------------------
        # BREAK MESSAGE
        # ----------------------------

        if take_break:

            cv2.putText(
                frame,
                recommendation,
                (20,470),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,255),
                2
            )

    else:

        cv2.putText(
            frame,
            "No Face Detected",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

    # ----------------------------
    # SHOW WINDOW
    # ----------------------------

    cv2.imshow(
        "DriveSafe AI",
        frame
    )

    key = cv2.waitKey(1)

    if key == 27:  # ESC
        break


# ----------------------------
# CLEANUP
# ----------------------------

cap.release()
cv2.destroyAllWindows()