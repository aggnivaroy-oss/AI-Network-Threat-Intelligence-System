from fastapi import APIRouter, HTTPException
from app.schemas.event import ThreatExplanation
from app.services.explanation import explanation_service
from typing import List

router = APIRouter()

# Global state access (managed in main.py)
stats = {
    "total_packets": 0,
    "total_threats": 0,
    "severity_counts": {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
}
history = []

@router.get("/stats")
async def get_stats():
    return stats

@router.get("/history")
async def get_history():
    return history

@router.post("/explain", response_model=ThreatExplanation)
async def explain_threat(event_details: dict):
    severity = event_details.get("severity", "MEDIUM")
    details = event_details.get("details", {})
    explanation = await explanation_service.get_explanation(severity, details)
    return {"explanation": explanation}
