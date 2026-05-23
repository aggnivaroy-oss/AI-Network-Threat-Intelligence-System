from pydantic import BaseModel
from typing import Dict, Any, Optional

class NetworkEvent(BaseModel):
    timestamp: str
    src: str
    dst: str
    proto: str
    severity: str
    prediction: str
    probability: float
    attack_type: str
    details: Dict[str, Any]

class ThreatExplanation(BaseModel):
    explanation: str

class SystemStats(BaseModel):
    total_packets: int
    total_threats: int
    severity_counts: Dict[str, int]
