from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class ContextPushRequest(BaseModel):
    scope: Literal["category", "merchant", "customer", "trigger"]
    context_id: str
    version: int
    payload: Dict[str, Any]
    delivered_at: str


class ContextPushResponse(BaseModel):
    accepted: bool
    ack_id: str
    stored_at: str


class ContextErrorResponse(BaseModel):
    accepted: bool = False
    reason: str
    current_version: Optional[int] = None
    details: Optional[str] = None


class ActionModel(BaseModel):
    conversation_id: str
    merchant_id: str
    customer_id: Optional[str] = None
    send_as: Literal["vera", "merchant_on_behalf"]
    trigger_id: str
    template_name: str
    template_params: List[str] = Field(default_factory=list)
    body: str
    cta: str
    suppression_key: str
    rationale: str


class TickRequest(BaseModel):
    now: str
    available_triggers: List[str] = Field(default_factory=list)


class TickResponse(BaseModel):
    actions: List[ActionModel] = Field(default_factory=list)


class ReplyRequest(BaseModel):
    conversation_id: str
    merchant_id: Optional[str] = None
    customer_id: Optional[str] = None
    from_role: Literal["merchant", "customer"]
    message: str
    received_at: str
    turn_number: int


class ReplyResponse(BaseModel):
    action: Literal["send", "wait", "end"]
    body: Optional[str] = None
    wait_seconds: Optional[int] = None
    cta: Optional[str] = None
    rationale: str


class HealthzResponse(BaseModel):
    status: str = "ok"
    uptime_seconds: int
    contexts_loaded: Dict[str, int]


class MetadataResponse(BaseModel):
    team_name: str
    team_members: List[str]
    model: str
    approach: str
    contact_email: str
    version: str
    submitted_at: str
