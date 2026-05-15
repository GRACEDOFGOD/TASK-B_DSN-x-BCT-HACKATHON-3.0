"""
Pydantic schemas — request & response models
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum


# ── Enums ────────────────────────────────────────────────────────────────────

class IncomeLevel(str, Enum):
    low = "low"
    middle = "middle"
    high = "high"


class PriceSensitivity(str, Enum):
    very_high = "very_high"
    high = "high"
    medium = "medium"
    low = "low"


class RatingTendency(str, Enum):
    generous = "generous"
    honest = "honest"
    critical = "critical"
    extreme = "extreme"


class Confidence(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


# ── Sub-models ───────────────────────────────────────────────────────────────

class ReviewHistoryItem(BaseModel):
    product: str
    domain: str
    stars: int = Field(..., ge=1, le=5)


class ConversationTurn(BaseModel):
    role: Literal["user", "assistant"]
    content: str


# ── Request schemas ───────────────────────────────────────────────────────────

class PersonaInput(BaseModel):
    name: str = Field(..., example="Chukwuemeka Obi")
    age: int = Field(..., ge=10, le=100, example=28)
    gender: str = Field(..., example="Male")
    location: str = Field(..., example="Lagos, Nigeria")
    education: str = Field(..., example="BSc Computer Science")
    occupation: str = Field(..., example="Software Engineer")
    behavior_patterns: str = Field(
        ..., example="Detail-oriented. Researches before buying."
    )
    avg_rating_given: float = Field(3.5, ge=1.0, le=5.0)
    total_reviews: int = Field(0, ge=0)
    goals: str = Field(..., example="Best tech at fair price.")
    needs: str = Field(..., example="Speed, reliability, value")
    pain_points: str = Field(..., example="Slow delivery, poor support")
    motivations: str = Field(..., example="Quality and efficiency")
    values: str = Field(..., example="Transparency, reliability")
    income_level: IncomeLevel = IncomeLevel.middle
    price_sensitivity: PriceSensitivity = PriceSensitivity.medium
    rating_tendency: RatingTendency = RatingTendency.honest
    preferences: List[str] = Field(
        default_factory=list, example=["tech", "food", "music"]
    )
    review_history: List[ReviewHistoryItem] = Field(default_factory=list)


class RecommendRequest(BaseModel):
    persona: PersonaInput
    context: str = Field(
        default="",
        example="I want recommendations for this weekend"
    )
    num_recs: int = Field(default=10, ge=1, le=20)
    conversation_history: Optional[List[ConversationTurn]] = None
    is_cold_start: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "persona": {
                    "name": "Tunde Bakare",
                    "age": 19,
                    "gender": "Male",
                    "location": "Lagos, Nigeria",
                    "education": "Undergraduate Year 2",
                    "occupation": "University Student",
                    "behavior_patterns": "Budget-conscious, loves gaming and music.",
                    "avg_rating_given": 3.9,
                    "total_reviews": 112,
                    "goals": "Cheap food, free entertainment, gaming",
                    "needs": "Affordability, fun, speed",
                    "pain_points": "Expensive prices, data finishing fast",
                    "motivations": "Fun, affordability",
                    "values": "Value for money",
                    "income_level": "low",
                    "price_sensitivity": "very_high",
                    "rating_tendency": "extreme",
                    "preferences": ["gaming", "music", "cheap food"],
                    "review_history": [
                        {"product": "PUBG Mobile", "domain": "entertainment", "stars": 5},
                        {"product": "Indomie", "domain": "food", "stars": 5}
                    ]
                },
                "context": "Show me something fun for the weekend",
                "num_recs": 10
            }
        }


# ── Response schemas ──────────────────────────────────────────────────────────

class TasteProfile(BaseModel):
    top_domains: List[str]
    price_preference: str
    personality_type: str
    key_interests: List[str]
    avoid_tags: List[str]
    discovery_openness: str
    social_influence: str
    profile_summary: str


class RecommendationItem(BaseModel):
    rank: int
    item_name: str
    domain: str
    category: str
    why_fits: str
    confidence: str
    cross_domain_note: Optional[str] = ""


class MultiturnResponse(BaseModel):
    response: str
    action: str
    refined_context: str


class RecommendResponse(BaseModel):
    recommendations: List[RecommendationItem]
    agent_reasoning: str
    domains_covered: List[str]
    taste_profile: TasteProfile
    multiturn_response: Optional[MultiturnResponse] = None
    is_cold_start: bool
    total_items_scored: int
    persona_name: str


# ── Preset persona schema ─────────────────────────────────────────────────────

class PresetPersonaResponse(BaseModel):
    id: str
    name: str
    occupation: str
    location: str
    age: int
    income_level: str
    preferences: List[str]
    total_reviews: int
