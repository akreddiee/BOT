from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class VoiceProfile(BaseModel):
    tone: Optional[str] = None
    vocab_allowed: Optional[List[str]] = Field(default_factory=list)
    vocab_taboo: Optional[List[str]] = Field(default_factory=list)
    taboos: Optional[List[str]] = Field(default_factory=list)


class OfferTemplate(BaseModel):
    id: Optional[str] = None
    title: str
    value: Optional[str] = None
    audience: Optional[str] = None
    type: Optional[str] = None


class PeerStats(BaseModel):
    avg_rating: Optional[float] = None
    avg_reviews: Optional[int] = None
    avg_ctr: Optional[float] = None
    scope: Optional[str] = None


class DigestItem(BaseModel):
    id: str
    kind: str
    title: str
    source: str
    trial_n: Optional[int] = None
    patient_segment: Optional[str] = None
    summary: Optional[str] = None


class CategoryContextModel(BaseModel):
    slug: str
    offer_catalog: List[Dict[str, Any]] = Field(default_factory=list)
    voice: Dict[str, Any] = Field(default_factory=dict)
    peer_stats: Dict[str, Any] = Field(default_factory=dict)
    digest: List[Dict[str, Any]] = Field(default_factory=list)
    patient_content_library: List[Dict[str, Any]] = Field(default_factory=list)
    seasonal_beats: List[Dict[str, Any]] = Field(default_factory=list)
    trend_signals: List[Dict[str, Any]] = Field(default_factory=list)


class MerchantIdentity(BaseModel):
    name: str
    city: str
    locality: str
    place_id: Optional[str] = None
    verified: bool = False
    languages: List[str] = Field(default_factory=lambda: ["en", "hi"])
    owner_first_name: Optional[str] = None
    established_year: Optional[int] = None


class MerchantSubscription(BaseModel):
    status: str
    plan: Optional[str] = None
    days_remaining: Optional[int] = 0
    days_since_expiry: Optional[int] = None


class PerformanceSnapshot(BaseModel):
    window_days: int = 30
    views: int = 0
    calls: int = 0
    directions: int = 0
    ctr: float = 0.0
    leads: Optional[int] = 0
    delta_7d: Dict[str, Any] = Field(default_factory=dict)


class MerchantContextModel(BaseModel):
    merchant_id: str
    category_slug: str
    identity: Dict[str, Any] = Field(default_factory=dict)
    subscription: Dict[str, Any] = Field(default_factory=dict)
    performance: Dict[str, Any] = Field(default_factory=dict)
    offers: List[Dict[str, Any]] = Field(default_factory=list)
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list)
    customer_aggregate: Dict[str, Any] = Field(default_factory=dict)
    signals: List[str] = Field(default_factory=list)
    review_themes: List[Dict[str, Any]] = Field(default_factory=list)


class CustomerContextModel(BaseModel):
    customer_id: str
    merchant_id: str
    identity: Dict[str, Any] = Field(default_factory=dict)
    relationship: Dict[str, Any] = Field(default_factory=dict)
    state: str = "active"
    preferences: Dict[str, Any] = Field(default_factory=dict)
    consent: Dict[str, Any] = Field(default_factory=dict)


class TriggerContextModel(BaseModel):
    id: str
    scope: Literal["merchant", "customer"]
    kind: str
    source: Literal["external", "internal"]
    merchant_id: str
    customer_id: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    urgency: int = 1
    suppression_key: str
    expires_at: Optional[str] = None
