class SeverityService:
    @staticmethod
    def calculate(probability: float, features: dict) -> str:
        if probability < 0.4:
            return "LOW"
        elif probability < 0.7:
            return "MEDIUM"
        elif probability < 0.9:
            return "HIGH"
        else:
            return "CRITICAL"

    @staticmethod
    def get_attack_type(prediction: int, features: dict) -> str:
        if prediction == 0:
            return "Normal"
        
        # Simple mapping based on NSL-KDD style features
        if features.get('serror_rate', 0) > 0.5:
            return "DoS Attack"
        elif features.get('count', 0) > 100:
            return "Probe / Port Scan"
        else:
            return "Suspicious Behavior"

severity_service = SeverityService()
