from datetime import datetime


class BreakRecommendation:

    def __init__(self):
        self.session_start = datetime.now()
        self.high_risk_duration = 0

    def update(self, risk_score):

        if risk_score >= 60:
            self.high_risk_duration += 1
        else:
            self.high_risk_duration = max(0, self.high_risk_duration - 1)

    def recommend(self):

        session_minutes = (
            datetime.now() - self.session_start
        ).seconds / 60

        # Continuous fatigue
        if self.high_risk_duration >= 30:
            return (
                True,
                "⚠ Fatigue detected. Please take a break."
            )

        # Long drive reminder
        if session_minutes >= 120:
            return (
                True,
                "☕ You've been driving for 2 hours. Take a 15-minute break."
            )

        return (
            False,
            ""
        )