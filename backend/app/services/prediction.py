import joblib
import numpy as np
from app.core.config import settings

class PredictionService:
    def __init__(self):
        self.model = joblib.load(settings.MODEL_PATH)

    def predict(self, feature_vector):
        prediction = self.model.predict(feature_vector)[0]
        probability = self.model.predict_proba(feature_vector)[0]
        return int(prediction), float(probability[1])

prediction_service = PredictionService()
