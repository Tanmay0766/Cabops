from pydantic import BaseModel
from typing import List


class Priority(BaseModel):
    level: str
    summary: str
    reason: str


class Dispatch(BaseModel):
    strategy: str
    capacity_status: str
    next_step: str


class Messages(BaseModel):
    hr: str
    employees: str
    backup_driver: str


class Impact(BaseModel):
    affected_employees: int
    estimated_delay: str
    client_risk: str


class AIResponse(BaseModel):
    priority: Priority

    recommended_actions: List[str]

    dispatch: Dispatch

    messages: Messages

    manual_decisions: List[str]

    impact: Impact