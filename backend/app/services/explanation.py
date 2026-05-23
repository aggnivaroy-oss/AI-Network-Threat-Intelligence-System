import google.generativeai as genai
from app.core.config import settings

class ExplanationService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    async def get_explanation(self, severity: str, details: dict) -> str:
        if severity not in ["HIGH", "CRITICAL"]:
            return "Routine network activity monitored."

        if not self.model:
            return f"Automated Analysis: {severity} threat level detected. Patterns suggest potential network anomaly."

        prompt = f"As a cybersecurity AI, explain this {severity} threat. Network Metrics: {details}. Be concise, technical, and professional."
        try:
            # Note: In a real async environment, use the async version if available
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"AI Analysis Unavailable: {str(e)}"

explanation_service = ExplanationService()
