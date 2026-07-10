class RiskEngine:

    def __init__(self):

        self.risk_score = 0

        self.eye_weight = 3
        self.yawn_weight = 2
        self.distraction_weight = 2

        self.recovery = 1

    def calculate_risk(
    self,
    drowsy=False,
    yawning=False,
    head_pose="Forward"
    ):
        if drowsy:
            self.risk_score += self.eye_weight
        if yawning:
            self.risk_score += self.yawn_weight
        if head_pose in ["Looking Left", "Looking Right", "Looking Up", "Looking Down"]:
            self.risk_score += self.distraction_weight
        if (not drowsy) and (not yawning) and (head_pose == "Forward"):
            self.risk_score -= 5
        self.risk_score = max(0, min(100, self.risk_score))
        return self.risk_score

    def get_risk_level(self, score):

        if score < 30:
            return "LOW"

        elif score < 60:
            return "MEDIUM"

        elif score < 80:
            return "HIGH"

        else:
            return "CRITICAL"